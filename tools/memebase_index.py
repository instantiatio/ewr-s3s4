#!/usr/bin/env python3
"""Build, verify or query a derived index of Memebase engrams."""

import argparse
import json
import math
import os
import re
import stat
import sys
import tempfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from unicodedata import category
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SCHEMA_VERSION = 3
REQUIRED = ("id", "kind", "status")
TIME_FIELDS = ("starts_at", "ends_at")
SCALAR_FIELDS = (*REQUIRED, "date", *TIME_FIELDS, "title")
FIELDS = (*SCALAR_FIELDS, "navigation")
NAVIGATION_FIELDS = {"cue", "result", "label"}
FIELD_LINE = re.compile(r"([A-Za-z_][\w-]*):(?:[ \t]+(.*)|[ \t]*)$")
SEQUENCE_ITEM = re.compile(r"-(?: +|$)")
INVALID_YAML_CHAR = re.compile(r"[^\x09\x0a\x0d\x20-\x7e\x85\xa0-\ud7ff\ue000-\ufffd\U00010000-\U0010ffff]")
RAW_LINE_SEPARATOR = re.compile(r"[\x85\u2028\u2029]")
# Only an odd run of backslashes introduces a Unicode escape.
SURROGATE_ESCAPE = re.compile(r"(?<!\\)(?:\\\\)*\\u[dD][89a-fA-F][0-9a-fA-F]{2}")
INDEX_YAML_ESCAPE = re.compile(r"[\x7f-\x9f\u2028\u2029\ufeff\ufffe\uffff]")
DOUBLE_QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"')
DOUBLE_QUOTED_ESCAPE = re.compile(r"\\(?:x[0-9a-fA-F]{2}|U[0-9a-fA-F]{8}|.)|\t")
YAML_TO_JSON_ESCAPES = {
    r"\0": r"\u0000", r"\a": r"\u0007", r"\v": r"\u000b", r"\e": r"\u001b",
    r"\ ": " ", r"\N": r"\u0085", r"\_": r"\u00a0", r"\L": r"\u2028", r"\P": r"\u2029",
    "\t": r"\t", "\\\t": r"\t",
}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:\d{2})$")


def unique_keys(items):
    fields = {}
    for key, value in items:
        if key in fields:
            raise ValueError(f"duplicate field {key}")
        fields[key] = value
    return fields


def nonfinite(value):
    raise ValueError(f"non-finite number {value}")


JSON = json.JSONDecoder(object_pairs_hook=unique_keys, parse_constant=nonfinite)


def json_escape(match):
    """Translate YAML-only escapes before decoding a double-quoted scalar."""
    token = match[0]
    if len(token) > 2:
        codepoint = int(token[2:], 16)
        if 0xD800 <= codepoint <= 0xDFFF or codepoint > 0x10FFFF:
            raise ValueError("invalid Unicode escape in YAML scalar")
        return json.dumps(chr(codepoint))[1:-1]
    return YAML_TO_JSON_ESCAPES.get(token, token)


def check_unicode_escapes(text):
    # A JSON decoder combines a UTF-16 pair before callers can inspect it.
    if SURROGATE_ESCAPE.search(text):
        raise ValueError("surrogate escape in YAML string; write the Unicode character directly")


def scalar(raw):
    """Read a portable YAML scalar or a JSON-form collection."""
    raw = raw.strip(" \t")
    if raw.startswith(("{", "[")):
        value, end = JSON.raw_decode(raw)
    elif raw.startswith('"'):
        match = DOUBLE_QUOTED.match(raw)
        if match is None:
            raise ValueError("unterminated quoted scalar")
        value = JSON.decode(DOUBLE_QUOTED_ESCAPE.sub(json_escape, match[0]))
        end = match.end()
    elif raw.startswith("'"):
        match = re.match(r"'((?:[^']|'')*)'", raw)
        if match is None:
            raise ValueError("unterminated quoted scalar")
        value, end = match[1].replace("''", "'"), match.end()
    else:
        value = re.split(r"(?:^|[ \t]+)#", raw, maxsplit=1)[0].rstrip(" \t")
        if not value or value in ("~", "null", "Null", "NULL"):
            return None
        if value in ("true", "True", "TRUE", "false", "False", "FALSE"):
            return value.lower() == "true"
        if re.fullmatch(r"[+-]?[0-9]+", value):
            return int(value)
        if re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value):
            number = float(value)
            return number if math.isfinite(number) else nonfinite(value)
        if (value[0] in "{[|>&*!%@`,]}" or re.match(r"[-?:](?:[ \t]|$)", value)
                or re.search(r":(?:[ \t]|$)", value)
                or re.fullmatch(r"[+-]?(?:0x[\da-fA-F]+|0o[0-7]+|\.inf|\.nan)", value, re.I)):
            raise ValueError("use a portable YAML scalar or JSON-form value")
        return value
    if raw.startswith(('"', "{", "[")):
        check_unicode_escapes(raw[:end])
    if raw[end:].strip(" \t") and not re.match(r"[ \t]+#", raw[end:]):
        raise ValueError("unexpected content after quoted value")
    return value


def portable_mapping(text):
    """Read block mappings and sequences in the portable YAML profile."""
    lines = [(len(line) - len(line.lstrip(" ")), line.lstrip(" "))
             for line in text.split("\n")
             if line.strip(" \t") and not line.lstrip(" \t").startswith("#")]

    def read_block(offset, depth=0):
        if depth > 50:
            raise ValueError("front matter nesting exceeds portable profile")
        indent, first = lines[offset]
        sequence = SEQUENCE_ITEM.match(first) is not None
        items = []
        while offset < len(lines) and lines[offset][0] == indent:
            _, line = lines[offset]
            if sequence:
                marker = SEQUENCE_ITEM.match(line)
                if marker is None:
                    break
                content = line[marker.end():]
                key, raw = None, content.strip(" \t")
                if FIELD_LINE.fullmatch(content.rstrip(" \t")) or SEQUENCE_ITEM.match(content):
                    lines[offset] = (indent + marker.end(), content.rstrip(" \t"))
                    value, offset = read_block(offset, depth+1)
                    items.append(value)
                    continue
            else:
                match = FIELD_LINE.fullmatch(line)
                if match is None:
                    raise ValueError("unsupported YAML block. Use JSON-form YAML for this value")
                key, raw = match[1], (match[2] or "").strip(" \t")
            offset += 1
            next_item = lines[offset] if offset < len(lines) else None
            indentless_list = (not sequence and next_item and next_item[0] == indent
                               and SEQUENCE_ITEM.match(next_item[1]))
            if (not raw or raw.startswith("#")) and next_item and (next_item[0] > indent or indentless_list):
                value, offset = read_block(offset, depth+1)
            else:
                value = scalar(raw)
            items.append(value if sequence else (key, value))
        return (items if sequence else unique_keys(items)), offset

    if not lines:
        return {}
    if lines[0][0]:
        raise ValueError("expected an unindented mapping")
    fields, offset = read_block(0)
    if offset != len(lines):
        raise ValueError("unexpected indentation. Use JSON-form YAML for this value")
    return fields


def read_metadata(path):
    try:
        with path.open(encoding="utf-8-sig") as source:
            if source.readline().rstrip("\r\n") != "---":
                raise ValueError("missing YAML front matter")
            lines = []
            for line in source:
                if line.rstrip("\r\n") in ("---", "..."):
                    break
                lines.append(line)
            else:
                raise ValueError("unterminated YAML front matter")
        text = "".join(lines)
        invalid = INVALID_YAML_CHAR.search(text)
        if invalid:
            raise ValueError(f"invalid raw YAML character U+{ord(invalid[0]):04X} in front matter")
        separator = RAW_LINE_SEPARATOR.search(text)
        if separator:
            raise ValueError(f"raw U+{ord(separator[0]):04X} is outside the portable single-line profile")
        if text.lstrip(" \t\r\n").startswith("{"):
            check_unicode_escapes(text)
            fields = JSON.decode(text)
        else:
            fields = portable_mapping(text)
        if not isinstance(fields, dict):
            raise ValueError("front matter must be a mapping")
        # Reject values that cannot be represented by the JSON-form index.
        json.dumps(fields, allow_nan=False)
        validate_fields(query_view({"metadata": fields, "path": path.name}))
        validate_metadata(fields)
        return fields
    except (UnicodeError, ValueError, RecursionError) as error:
        raise ValueError(f"{path.name}: {error}") from error


def query_view(entry):
    fields = entry["metadata"]
    defaults = {"title": Path(entry["path"]).stem, "navigation": []}
    result = {}
    for key in FIELDS:
        value = fields.get(key)
        if value is None:
            value = defaults.get(key)
        if value is not None:
            result[key] = value
    result["path"] = entry["path"]
    return result


def parse_time(value):
    if DATE.fullmatch(value):
        return date.fromisoformat(value)
    if TIMESTAMP.fullmatch(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError(f"expected a date or an ISO timestamp with offset, got {value!r}")


def is_single_line_text(value):
    return isinstance(value, str) and all(char.isprintable() or category(char) == "Zs" for char in value)


def validate_fields(fields):
    for key in (*REQUIRED, "title"):
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            raise ValueError(f"missing or empty {key}")
    for key in SCALAR_FIELDS:
        value = fields.get(key)
        if value is not None and not is_single_line_text(value):
            raise ValueError(f"invalid {key}")
    navigation = fields.get("navigation")
    if not isinstance(navigation, list):
        raise ValueError("navigation must be a JSON-compatible list")
    for hint in navigation:
        if not isinstance(hint, dict) or "cue" not in hint or hint.keys() - NAVIGATION_FIELDS:
            raise ValueError("each navigation item must have a cue and may have a result or label")
        if any(not is_single_line_text(value) or not value.strip() for value in hint.values()):
            raise ValueError("navigation values must be nonempty single-line text")
    if fields.get("date") is not None:
        if not DATE.fullmatch(fields["date"]):
            raise ValueError("date must use YYYY-MM-DD")
        date.fromisoformat(fields["date"])
    start = parse_time(fields["starts_at"]) if fields.get("starts_at") is not None else None
    end = parse_time(fields["ends_at"]) if fields.get("ends_at") is not None else None
    if end is not None and (start is None or type(end) is not type(start) or end < start):
        raise ValueError("ends_at requires starts_at at the same precision and cannot precede it")


def validate_metadata(fields):
    def optional_date(value, key):
        if value is not None:
            if not isinstance(value, str) or not DATE.fullmatch(value):
                raise ValueError(f"{key} must use YYYY-MM-DD")
            date.fromisoformat(value)

    for key in ("last_used", "importance_assessed_on"):
        optional_date(fields.get(key), key)
    uses = fields.get("use_count")
    if uses is not None and (type(uses) is not int or uses < 0):
        raise ValueError("use_count must be a nonnegative integer")
    events = fields.get("use_events")
    if events is not None and (not isinstance(events, list) or any(not isinstance(x, str) or not x for x in events)):
        raise ValueError("use_events must be a list of event IDs")
    rating = fields.get("importance")
    if rating is not None and rating not in ("very-important", "important", "neutral", "not-important"):
        raise ValueError("invalid importance")
    for key in ("applies_when", "basis"):
        if fields.get(key) is not None and not isinstance(fields[key], str):
            raise ValueError(f"{key} must be text")
    if fields.get("capture") is not None and not isinstance(fields["capture"], dict):
        raise ValueError("capture must be a mapping")
    claims = fields.get("time_sensitive")
    if claims is not None:
        if not isinstance(claims, list):
            raise ValueError("time_sensitive must be a list of claims")
        for claim in claims:
            if not isinstance(claim, dict) or not isinstance(claim.get("claim"), str) or not claim["claim"].strip():
                raise ValueError("time_sensitive items require claim text")
            for key in ("checked_on", "valid_until", "review_after"):
                optional_date(claim.get(key), f"time_sensitive.{key}")


def inside_file(root, name, scope=None):
    path = (root / name).resolve(strict=True)
    if not path.is_relative_to(scope or root):
        raise ValueError(f"path must resolve inside the connected memory scope: {name}")
    if not path.is_file():
        raise ValueError(f"expected a regular file: {name}")
    return path


def signature(metadata):
    return [metadata.st_dev, metadata.st_ino, metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_size]


def scan(root):
    engrams = root / "Engrams"
    scope = engrams.resolve(strict=True)
    if scope == root or not scope.is_relative_to(root) or not engrams.is_dir():
        raise ValueError("Engrams must be a directory inside the connected Memebase")

    def walk_error(error):
        raise error

    sources = {}
    for directory, _, names in os.walk(engrams, onerror=walk_error, followlinks=False):
        for name in names:
            path = Path(directory) / name
            if path.suffix != ".md":
                continue
            metadata = path.lstat()
            if stat.S_ISREG(metadata.st_mode):
                relative = path.relative_to(root).as_posix()
                inside_file(root, relative, scope)
                sources[relative] = signature(metadata)
    return sources


def rows_from_sources(root, sources):
    rows, ids = [], set()
    scope = (root / "Engrams").resolve(strict=True)
    for relative, stamp in sorted(sources.items()):
        path = inside_file(root, relative, scope)
        fields = read_metadata(path)
        if signature(path.lstat()) != stamp:
            raise ValueError("an engram changed while reading the index; retry")
        if fields["id"] in ids:
            raise ValueError(f"duplicate engram ID {fields['id']!r}: {relative}")
        ids.add(fields["id"])
        rows.append({"path": relative, "metadata": fields})
    return rows


def encoded_index(rows):
    text = json.dumps({"schema_version": SCHEMA_VERSION, "entries": rows}, ensure_ascii=False, indent=2)
    # JSON permits literals that YAML readers reject or treat as line breaks.
    return INDEX_YAML_ESCAPE.sub(lambda match: f"\\u{ord(match[0]):04x}", text) + "\n"


def write_index(path, text, root, sources):
    with tempfile.TemporaryDirectory(prefix=".memebase-index-", dir=root) as directory:
        staged = Path(directory) / path.name
        with staged.open("w", encoding="utf-8", newline="\n") as output:
            output.write(text)
            output.flush()
            os.fsync(output.fileno())
        if scan(root) != sources or path.is_symlink():
            raise ValueError("Memebase changed while building the index; retry")
        os.replace(staged, path)


def bounds(args):
    if args.on:
        if args.first or args.until:
            raise ValueError("choose --on or --from with --until")
        day = date.fromisoformat(args.on)
        return day, day + timedelta(days=1)
    if args.first or args.until:
        if not args.first or not args.until:
            raise ValueError("--from and --until must be used together")
        start, stop = date.fromisoformat(args.first), date.fromisoformat(args.until)
        if start >= stop:
            raise ValueError("--until must follow --from; the end is exclusive")
        return start, stop
    return None


def in_period(row, period, zone):
    if "starts_at" not in row:
        return False
    start = parse_time(row["starts_at"])
    finish = parse_time(row["ends_at"]) if "ends_at" in row else start
    lower, upper = period
    if isinstance(start, datetime):
        start, finish = start.astimezone(timezone.utc), finish.astimezone(timezone.utc)
        lower = datetime.combine(lower, time.min, zone).astimezone(timezone.utc)
        upper = datetime.combine(upper, time.min, zone).astimezone(timezone.utc)
    if start == finish:
        return lower <= start < upper
    return start < upper and lower < finish


def matches_text(row, needle):
    return needle in row["title"].casefold() or any(
        needle in value.casefold() for hint in row["navigation"] for value in hint.values()
    )


def query_rows(rows, args):
    period = bounds(args)
    if period and not args.timezone:
        raise ValueError("a date query requires an explicit --timezone")
    zone = ZoneInfo(args.timezone) if args.timezone else timezone.utc
    needle = args.text.casefold() if args.text else None
    matches = []
    for entry in rows:
        row = query_view(entry)
        if (args.id and row["id"] != args.id) or (args.kind and row["kind"] != args.kind):
            continue
        if not (args.id or args.history) and row["status"] != "active":
            continue
        if needle and not matches_text(row, needle):
            continue
        if period is None or in_period(row, period, zone):
            matches.append((row, entry))
    if period:
        def order(row):
            start = parse_time(row["starts_at"])
            if not isinstance(start, datetime):
                start = datetime.combine(start, time.min, zone)
            return start.astimezone(timezone.utc), row["id"]

        matches.sort(key=lambda pair: order(pair[0]))
    if not getattr(args, "fields", None):
        return [row for row, _ in matches]
    result = []
    for row, entry in matches:
        values = {**row, **entry["metadata"], "path": row["path"], "metadata": entry["metadata"]}
        result.append({key: values[key] for key in args.fields if key in values})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memebase", type=Path)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("build", help="rebuild Index.yaml from the engrams")
    commands.add_parser("check", help="compare Index.yaml to the current engrams")
    query = commands.add_parser("query", help="find source records by ID, kind, navigation text or local date range")
    query.add_argument("--id")
    query.add_argument("--kind")
    query.add_argument("--text", help="look for literal text in titles and navigation hints")
    query.add_argument("--on", metavar="YYYY-MM-DD")
    query.add_argument("--from", dest="first", metavar="YYYY-MM-DD")
    query.add_argument("--until", metavar="YYYY-MM-DD")
    query.add_argument("--timezone", help="IANA zone used for the date range")
    query.add_argument("--history", action="store_true", help="include inactive entries")
    query.add_argument("--fields", nargs="+", metavar="FIELD", help="return selected source fields, path or the complete metadata mapping")
    args = parser.parse_args()
    try:
        root = args.memebase.resolve(strict=True)
        path = root / "Index.yaml"
        if path.is_symlink():
            raise ValueError("Index.yaml must be a regular file in Memebase")
        sources = scan(root)
        # Even unchanged file signatures cannot authenticate edited index values.
        rows = rows_from_sources(root, sources)
        if scan(root) != sources:
            raise ValueError("Memebase changed while reading the index; retry")
        if args.action == "query":
            print(json.dumps(query_rows(rows, args), ensure_ascii=False, indent=2))
        elif args.action == "build":
            write_index(path, encoded_index(rows), root, sources)
            print(f"Indexed {len(rows)} engrams")
        elif not path.is_file() or path.read_bytes() != encoded_index(rows).encode("utf-8"):
            raise ValueError("Index.yaml is missing or stale; rebuild it from the engrams")
        else:
            print(f"Index.yaml matches {len(rows)} engrams")
    except (OSError, UnicodeError, ValueError, OverflowError, ZoneInfoNotFoundError) as error:
        parser.exit(1, f"Memebase index: {error}\n")


if __name__ == "__main__":
    main()

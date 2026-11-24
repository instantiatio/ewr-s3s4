#!/usr/bin/env python3
"""Build, verify or query a derived index of Memebase engrams."""

import argparse
import json
import os
import posixpath
import re
import stat
import string
import sys
import tempfile
import unicodedata
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SCHEMA_VERSION = 2
REQUIRED = ("id", "kind", "status")
TIME_FIELDS = ("starts_at", "ends_at")
SCALAR_FIELDS = (*REQUIRED, "date", *TIME_FIELDS, "title")
FIELDS = (*SCALAR_FIELDS, "navigation")
PROJECTION_FIELDS = ("last_used", "use_count", "importance")
NAVIGATION_FIELDS = {"cue", "result", "label"}
FIELD_LINE = re.compile(r"([A-Za-z_][\w-]*):(?:[ \t]+(.*)|[ \t]*)$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:\d{2})$")
REFERENCE_HEAD = re.compile(r"^ {0,3}\[((?:\\.|[^\[\]\\\n])+)\]:[ \t]*")
LINK_TITLE = r"""(?:"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|\((?:\\.|[^()\\\n])*\))"""
INLINE_END = re.compile(rf"(?:[ \t]+{LINK_TITLE})?[ \t]*\)")
DEFINITION_END = re.compile(rf"(?:[ \t]+{LINK_TITLE})?[ \t]*\Z")
LABEL = r"(?:\\.|[^\[\]\\\n])+"
REFERENCE_TAIL = re.compile(rf"\[((?:{LABEL})?)\]")
BRACKET_TOKEN = re.compile(r"\\[^\n]|!?\[|\]|\n")
FENCE = re.compile(r"^ {0,3}(?:\x60{3,}(?!\x60)[^\x60\n]*|~{3,}[^\n]*)$")
MARKER = re.compile(r"\x60{3,}|~{3,}")
QUOTE = re.compile(r" {0,3}>[ \t]?")
LIST_MARKER = re.compile(r"^ {0,3}(?:[-+*]|(?P<number>\d{1,9})[.)])[ \t]{1,4}(?=\S)")
BACKTICKS = re.compile(r"`+")
INLINE_TOKEN = re.compile(r"\\[^\n]|`+|\[|\]")
ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
BLOCK_RULE = re.compile(r"^ {0,3}(?:=+|-+|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})[ \t]*$")
IMPORTANCE = re.compile(r"^ {0,3}##[ \t]+(?:Важность|Importance)[ \t]*$\n(.*?)(?=^ {0,3}#{1,2}[ \t]|\Z)", re.M | re.S | re.I)
RATING_LINE = re.compile(r"(?i)(?:оценка|rating|évaluation)\s*[.:]\s*(.+)")
ESCAPABLE = frozenset(string.punctuation)
ESCAPED_PUNCTUATION = re.compile(r"\\([" + re.escape(string.punctuation) + "])")
IMPORTANCE_VALUES = {"very-important", "important", "neutral", "not-important"}
RATINGS = {
    "very important": "very-important", "очень важно": "very-important", "très important": "very-important",
    "important": "important", "важно": "important",
    "neutral": "neutral", "нейтрально": "neutral", "neutre": "neutral",
    "not important": "not-important", "не важно": "not-important", "неважно": "not-important",
    "peu important": "not-important", "pas important": "not-important",
}


def scalar(raw):
    """Read the plain or quoted, single-line scalars used for indexed fields."""
    raw = raw.strip()
    if raw.startswith('"'):
        value, end = json.JSONDecoder().raw_decode(raw)
    elif raw.startswith("'"):
        match = re.match(r"'((?:[^']|'')*)'", raw)
        if match is None:
            raise ValueError("unterminated quoted scalar")
        value, end = match[1].replace("''", "'"), match.end()
    else:
        value = re.split(r"(?:^|[ \t]+)#", raw, maxsplit=1)[0].rstrip()
        if not value or value in ("~", "null", "Null", "NULL"):
            return None
        if value[0] in "[{|>&*!%@`" or value.startswith(("- ", "? ", ": ")) or ": " in value:
            raise ValueError("expected a plain or quoted single-line scalar")
        return value
    if raw[end:].strip() and not re.match(r"[ \t]+#", raw[end:]):
        raise ValueError("unexpected content after quoted scalar")
    return value


def read_engram(path, *, with_body=False):
    try:
        with path.open(encoding="utf-8-sig") as source:
            if source.readline().rstrip("\r\n") != "---":
                raise ValueError("missing YAML front matter")
            fields = {}
            for line in source:
                line = line.rstrip("\r\n")
                if line in ("---", "..."):
                    break
                match = FIELD_LINE.fullmatch(line)
                if match is None or match[1] not in (*FIELDS, *PROJECTION_FIELDS):
                    continue
                key = match[1]
                if key in fields:
                    raise ValueError(f"duplicate field {key}")
                value = match[2] or ""
                if key in PROJECTION_FIELDS and not with_body:
                    continue
                fields[key] = json.loads(value) if key == "navigation" else scalar(value)
            else:
                raise ValueError("unterminated YAML front matter")
            body = source.read().strip("\n") if with_body else None
        fields.setdefault("title", path.stem)
        fields.setdefault("navigation", [])
        validate_fields(fields)
        projected = {key: fields[key] for key in FIELDS if fields.get(key) is not None}
        if with_body:
            last_used = fields.get("last_used")
            if last_used is not None:
                if not DATE.fullmatch(last_used):
                    raise ValueError("last_used must use YYYY-MM-DD")
                date.fromisoformat(last_used)
                projected["last_used"] = last_used
            use_count = fields.get("use_count")
            if use_count is not None and re.fullmatch(r"[0-9]+", use_count):
                projected["use_count"] = int(use_count)
            importance = fields.get("importance")
            if importance is not None:
                if importance not in IMPORTANCE_VALUES:
                    raise ValueError("invalid importance; expected a canonical rating")
                projected["importance"] = importance
        return projected, body
    except (UnicodeError, ValueError) as error:
        raise ValueError(f"{path.name}: {error}") from error


def blank(text):
    return re.sub(r"[^\n]", " ", text)


def destination_at(text, start):
    """Return a single-line destination and its end, retaining Markdown escapes."""
    angled = text.startswith("<", start)
    begin = start + int(angled)
    cursor = begin
    depth = 0
    while cursor < len(text):
        char = text[cursor]
        if char == "\\" and text[cursor+1:cursor+2] in ESCAPABLE:
            cursor += 2
            continue
        if angled:
            if char == ">":
                return text[begin:cursor], cursor + 1
            if char in "<\n":
                return None
        elif char.isspace() or ord(char) < 32:
            break
        elif char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                break
            depth -= 1
        cursor += 1
    if not angled and not depth:
        return text[begin:cursor], cursor
    return None


def link_tail(text, start, *, definition=False):
    if not definition:
        if not text.startswith("(", start):
            return None
        start += 1
        while start < len(text) and text[start] in " \t":
            start += 1
    parsed = destination_at(text, start)
    if parsed is None:
        return None
    destination, end = parsed
    if definition and end == start:
        return None
    suffix = (DEFINITION_END if definition else INLINE_END).match(text, end)
    if suffix:
        return destination, suffix.end()
    return None


def reference_definition(line):
    head = REFERENCE_HEAD.match(line)
    if head and (tail := link_tail(line, head.end(), definition=True)):
        return reference_key(head[1]), tail[0]
    return None


def mask_code_spans(paragraph):
    """Hide complete spans within one inline block while preserving source offsets."""
    if "`" not in paragraph:
        return paragraph
    # A closing run is literal even after a backslash. Escapes matter only
    # while scanning for an opener. Index the next exact-length run up front.
    following = {}
    next_by_length = {}
    for run in reversed(list(BACKTICKS.finditer(paragraph))):
        length = run.end() - run.start()
        for start in (run.start(), run.start() + 1):
            closing = next_by_length.get(run.end() - start)
            if closing is not None:
                following[start] = closing
        next_by_length[length] = run.end()

    pieces = []
    copied = cursor = depth = 0
    while token := INLINE_TOKEN.search(paragraph, cursor):
        cursor = token.end()
        if token[0].startswith("`") and token.start() in following:
            cursor = following[token.start()]
            pieces.append(paragraph[copied:token.start()])
            # A span is content, so it cannot turn into Markdown whitespace.
            pieces.append(re.sub(r"[^\n]", "\x00", paragraph[token.start():cursor]))
            copied = cursor
        elif token[0] == "[":
            depth += 1
        elif token[0] == "]" and depth:
            depth -= 1
            if inline := link_tail(paragraph, cursor):
                cursor = inline[1]
            elif reference := REFERENCE_TAIL.match(paragraph, cursor):
                cursor = reference.end()
    pieces.append(paragraph[copied:])
    return "".join(pieces)


def visible_markdown(body, definitions=None):
    """Mask code and definitions at their block boundaries, keeping source offsets."""
    lines = []
    paragraph = []

    def flush():
        if paragraph:
            lines.append(mask_code_spans("".join(paragraph)))
            paragraph.clear()

    # Each open container consumes a quote marker or a list continuation indent.
    containers = []
    fence = ""
    for line in body.splitlines(keepends=True):
        content = line.rstrip("\n").expandtabs(4)
        matched = 0
        for indent in containers:
            if indent is None:
                quote = QUOTE.match(content)
                if not quote:
                    break
                content = content[quote.end():]
            elif content.startswith(" " * indent):
                content = content[indent:]
            elif content.strip():
                break
            matched += 1

        if matched < len(containers):
            # Unmarked paragraph continuations still belong to the open item
            # or quote. A definition cannot interrupt that paragraph.
            if (paragraph and content.strip() and not
                (QUOTE.match(content) or LIST_MARKER.match(content) or
                 ATX_HEADING.match(content) or BLOCK_RULE.fullmatch(content) or
                 FENCE.fullmatch(content))):
                paragraph.append(line)
                continue
            flush()
            del containers[matched:]
            fence = ""

        if fence:
            lines.append(blank(line))
            if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", content):
                fence = ""
            continue

        while True:
            quote = QUOTE.match(content)
            if quote:
                flush()
                containers.append(None)
                content = content[quote.end():]
                continue
            marker = LIST_MARKER.match(content)
            if not marker or BLOCK_RULE.fullmatch(content):
                break
            # An ordered list can interrupt a paragraph only at ordinal 1.
            number = marker['number']
            if paragraph and number and int(number) != 1:
                break
            flush()
            containers.append(marker.end())
            content = content[marker.end():]

        if FENCE.fullmatch(content):
            flush()
            fence = MARKER.search(content)[0]
            lines.append(blank(line))
        elif not content.strip() or (not paragraph and content.startswith("    ")):
            flush()
            lines.append(blank(line))
        elif ATX_HEADING.match(content) or (BLOCK_RULE.fullmatch(content) and
                                            (paragraph or not content.lstrip().startswith("="))):
            flush()
            lines.append(mask_code_spans(line))
        elif not paragraph and (definition := reference_definition(content)):
            if definitions is not None:
                key, destination = definition
                definitions.setdefault(key, destination)
            lines.append(blank(line))
        else:
            paragraph.append(line)
    flush()
    return "".join(lines)


def personal_importance(markdown):
    section = IMPORTANCE.search(markdown)
    if section:
        for line in section[1].splitlines():
            rating = RATING_LINE.fullmatch(unicodedata.normalize("NFC", line.strip().replace("**", "")))
            if rating:
                value = rating[1].strip().rstrip(".").casefold()
                return RATINGS.get(value, "unrated")
    return "unrated"


def reference_key(label):
    return " ".join(ESCAPED_PUNCTUATION.sub(r"\1", label).casefold().split())


def markdown_links(body, markdown=None, targets=None):
    if targets is None:
        targets = {}
        markdown = visible_markdown(body, targets)
    openings = []
    cursor = 0
    for token in BRACKET_TOKEN.finditer(markdown):
        if token.start() < cursor:
            continue
        if token[0] == "\n":
            openings.clear()
        elif token[0] in ("[", "!["):
            inside_image = bool(openings and openings[-1][3])
            is_image = token[0] == "!["
            openings.append((token.start(), token.end(), is_image, is_image or inside_image))
        elif token[0] == "]" and openings:
            start, label_start, is_image, inside_image = openings.pop()
            label = body[label_start:token.start()]
            end = token.end()
            inline = link_tail(markdown, end)
            reference = REFERENCE_TAIL.match(markdown, end) if inline is None else None
            if inline:
                destination, end = inline
            else:
                key = (reference[1] or label) if reference else label
                destination = targets.get(reference_key(key))
                if reference and (destination is not None or is_image):
                    end = reference.end()
            if destination is not None or is_image:
                cursor = end
            if destination is not None and not inside_image:
                # A resolved inner link prevents its enclosing label from becoming a second link.
                openings.clear()
                yield start, end, label, destination


def engram_paths(rows):
    return {unicodedata.normalize("NFC", row["path"]): row["id"] for row in rows}


def linked_engram(destination, relative, paths):
    destination = unquote(ESCAPED_PUNCTUATION.sub(r"\1", destination).split("#", 1)[0])
    target = posixpath.normpath(posixpath.join(posixpath.dirname(relative), destination))
    return paths.get(unicodedata.normalize("NFC", target))


def parse_time(value):
    if DATE.fullmatch(value):
        return date.fromisoformat(value)
    if TIMESTAMP.fullmatch(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError(f"expected a date or an ISO timestamp with offset, got {value!r}")


def validate_fields(fields):
    for key in (*REQUIRED, "title"):
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            raise ValueError(f"missing or empty {key}")
    for key in SCALAR_FIELDS:
        value = fields.get(key)
        if value is not None and (not isinstance(value, str) or not value.isprintable()):
            raise ValueError(f"invalid {key}")
    navigation = fields.get("navigation")
    if not isinstance(navigation, list):
        raise ValueError("navigation must be a JSON-compatible list")
    for hint in navigation:
        if not isinstance(hint, dict) or "cue" not in hint or hint.keys() - NAVIGATION_FIELDS:
            raise ValueError("each navigation item must have a cue and may have a result or label")
        if any(not isinstance(value, str) or not value.strip() or not value.isprintable() for value in hint.values()):
            raise ValueError("navigation values must be nonempty single-line text")
    if fields.get("date") is not None:
        if not DATE.fullmatch(fields["date"]):
            raise ValueError("date must use YYYY-MM-DD")
        date.fromisoformat(fields["date"])
    start = parse_time(fields["starts_at"]) if fields.get("starts_at") is not None else None
    end = parse_time(fields["ends_at"]) if fields.get("ends_at") is not None else None
    if end is not None and (start is None or type(end) is not type(start) or end < start):
        raise ValueError("ends_at requires starts_at at the same precision and cannot precede it")


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


def rows_from_sources(root, sources, *, expanded=False):
    rows, ids = [], set()
    bodies = {}
    scope = (root / "Engrams").resolve(strict=True)
    for relative, stamp in sorted(sources.items()):
        path = inside_file(root, relative, scope)
        fields, body = read_engram(path, with_body=expanded)
        if signature(path.lstat()) != stamp:
            raise ValueError("an engram changed while reading the index; retry")
        if fields["id"] in ids:
            raise ValueError(f"duplicate engram ID {fields['id']!r}: {relative}")
        ids.add(fields["id"])
        rows.append({**fields, "path": relative, "source": stamp})
        if expanded:
            bodies[relative] = body
    if expanded:
        paths = engram_paths(rows)
        for row in rows:
            body = bodies[row["path"]]
            targets = {}
            markdown = visible_markdown(body, targets)
            if "importance" not in row:
                row["importance"] = personal_importance(markdown)
            links = (linked_engram(dest, row["path"], paths) for _, _, _, dest in markdown_links(body, markdown, targets))
            row["links"] = list(dict.fromkeys(target for target in links if target is not None))
    return rows


def encoded_index(rows):
    return json.dumps({"schema_version": SCHEMA_VERSION, "entries": rows}, ensure_ascii=False, indent=2) + "\n"


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
    for row in rows:
        if (args.id and row["id"] != args.id) or (args.kind and row["kind"] != args.kind):
            continue
        if not (args.id or args.history) and row["status"] != "active":
            continue
        if needle and not matches_text(row, needle):
            continue
        if period is None or in_period(row, period, zone):
            matches.append({key: value for key, value in row.items() if key != "source"})
    if period:
        def order(row):
            start = parse_time(row["starts_at"])
            if not isinstance(start, datetime):
                start = datetime.combine(start, time.min, zone)
            return start.astimezone(timezone.utc), row["id"]

        matches.sort(key=order)
    return matches


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
    args = parser.parse_args()
    try:
        root = args.memebase.resolve(strict=True)
        path = root / "Index.yaml"
        if path.is_symlink():
            raise ValueError("Index.yaml must be a regular file in Memebase")
        sources = scan(root)
        # Even unchanged file signatures cannot authenticate edited index values.
        rows = rows_from_sources(root, sources, expanded=args.action != "query")
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

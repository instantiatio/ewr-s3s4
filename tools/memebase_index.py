#!/usr/bin/env python3
"""Build, verify or query a derived index of Memebase engrams."""

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


REQUIRED = ("id", "kind", "status")
TIME_FIELDS = ("starts_at", "ends_at")
FIELDS = (*REQUIRED, "date", *TIME_FIELDS)
FIELD_LINE = re.compile(r"([A-Za-z_][\w-]*):(?:[ \t]+(.*)|[ \t]*)$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:\d{2})$")


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


def read_fields(path):
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
                if match is None or match[1] not in FIELDS:
                    continue
                key = match[1]
                if key in fields:
                    raise ValueError(f"duplicate field {key}")
                fields[key] = scalar(match[2] or "")
            else:
                raise ValueError("unterminated YAML front matter")
        validate_fields(fields)
        return {key: fields[key] for key in FIELDS if fields.get(key) is not None}
    except (UnicodeError, ValueError) as error:
        raise ValueError(f"{path.name}: {error}") from error


def parse_time(value):
    if DATE.fullmatch(value):
        return date.fromisoformat(value)
    if TIMESTAMP.fullmatch(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError(f"expected a date or an ISO timestamp with offset, got {value!r}")


def validate_fields(fields):
    for key in REQUIRED:
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            raise ValueError(f"missing or empty {key}")
    for key in FIELDS:
        value = fields.get(key)
        if value is not None and (not isinstance(value, str) or not value.isprintable()):
            raise ValueError(f"invalid {key}")
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


def rows_from_sources(root, sources):
    rows, ids = [], set()
    scope = (root / "Engrams").resolve(strict=True)
    for relative, stamp in sorted(sources.items()):
        path = inside_file(root, relative, scope)
        fields = read_fields(path)
        if signature(path.lstat()) != stamp:
            raise ValueError("an engram changed while reading the index; retry")
        if fields["id"] in ids:
            raise ValueError(f"duplicate engram ID {fields['id']!r}: {relative}")
        ids.add(fields["id"])
        rows.append({**fields, "path": relative, "source": stamp})
    return rows


def encoded_index(rows):
    return json.dumps({"schema_version": 1, "entries": rows}, ensure_ascii=False, indent=2) + "\n"


def cached_rows(path, sources):
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        if document["schema_version"] != 1 or not isinstance(document["entries"], list):
            return None
        rows = document["entries"]
        times = {row["path"]: row["source"] for row in rows}
        if len(times) != len(rows) or times != sources or len({row["id"] for row in rows}) != len(rows):
            return None
        for row in rows:
            validate_fields(row)
        return rows
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError):
        return None


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


def query_rows(rows, args):
    period = bounds(args)
    if period and not args.timezone:
        raise ValueError("a date query requires an explicit --timezone")
    zone = ZoneInfo(args.timezone) if args.timezone else timezone.utc
    matches = []
    for row in rows:
        if (args.id and row["id"] != args.id) or (args.kind and row["kind"] != args.kind):
            continue
        if not (args.id or args.history) and row["status"] != "active":
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
    query = commands.add_parser("query", help="find entries by ID, kind or local date range")
    query.add_argument("--id")
    query.add_argument("--kind")
    query.add_argument("--on", metavar="YYYY-MM-DD")
    query.add_argument("--from", dest="first", metavar="YYYY-MM-DD")
    query.add_argument("--until", metavar="YYYY-MM-DD")
    query.add_argument("--timezone", help="IANA zone used for the date range")
    query.add_argument("--history", action="store_true", help="include inactive entries")
    args = parser.parse_args()
    try:
        root = args.memebase.resolve(strict=True)
        inside_file(root, "Index.md")
        path = root / "Index.yaml"
        if path.is_symlink():
            raise ValueError("Index.yaml must be a regular file in Memebase")
        sources = scan(root)
        rows = cached_rows(path, sources) if args.action == "query" else None
        if rows is None:
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

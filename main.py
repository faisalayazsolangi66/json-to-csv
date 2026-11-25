#!/usr/bin/env python3
"""Convert a JSON array of objects to CSV.

Reads a JSON file whose top level is a list of objects and writes a
CSV file with one column per key. Columns follow the key order of
the first object, with any extra keys from later objects appended.
Nested values (lists/dicts) are serialised as compact JSON strings.
"""
import argparse
import csv
import json
import sys


def load_rows(input_path, encoding="utf-8"):
    """Load a JSON array of objects from *input_path*."""
    with open(input_path, encoding=encoding) as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        # Allow {"key": [...]} style wrappers with a single list value.
        lists = [value for value in data.values() if isinstance(value, list)]
        if len(lists) == 1:
            data = lists[0]
    if not isinstance(data, list):
        raise ValueError("top-level JSON must be an array of objects")
    rows = [item for item in data if isinstance(item, dict)]
    if len(rows) != len(data):
        raise ValueError("every item in the JSON array must be an object")
    if not rows:
        raise ValueError("JSON array is empty; nothing to convert")
    return rows


def columns_for(rows):
    """Column names in first-seen order across all rows."""
    columns = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    return columns


def convert(rows, output_path, delimiter=",", encoding="utf-8"):
    """Write *rows* as CSV to *output_path* (or stdout if None)."""
    columns = columns_for(rows)
    handle = (open(output_path, "w", newline="", encoding=encoding)
              if output_path else sys.stdout)
    try:
        writer = csv.DictWriter(handle, fieldnames=columns,
                                delimiter=delimiter, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: (json.dumps(value, ensure_ascii=False)
                      if isinstance(value, (dict, list)) else value)
                for key, value in row.items()
            })
    finally:
        if output_path:
            handle.close()
    return columns


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert a JSON array of objects to CSV.")
    parser.add_argument("input", help="input JSON file")
    parser.add_argument("-o", "--output",
                        help="output CSV file (default: print to stdout)")
    parser.add_argument("--delimiter", default=",",
                        help="CSV field delimiter (default: ',')")
    parser.add_argument("--encoding", default="utf-8",
                        help="file encoding (default: utf-8)")
    args = parser.parse_args(argv)

    try:
        rows = load_rows(args.input, encoding=args.encoding)
    except FileNotFoundError:
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    columns = convert(rows, args.output, delimiter=args.delimiter,
                      encoding=args.encoding)
    if args.output:
        print(f"Converted {len(rows)} row(s), {len(columns)} column(s): "
              f"{args.input} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

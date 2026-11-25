# JSON to CSV

Convert a JSON array of objects to CSV. Columns follow the key
order of the first object, with any extra keys from later objects
appended. Nested values (lists and objects) are written as compact
JSON strings. Output goes to a file with `-o`, or to standard
output when no output file is given.

## Requirements

- Python 3 (standard library only, no extra packages)

## Usage

```bash
python3 main.py data.json
python3 main.py data.json -o data.csv
python3 main.py data.json -o data.csv --delimiter ";"
```

## Example

```bash
$ cat people.json
[{"name": "Ayesha", "age": 28, "city": "Lahore"}, {"name": "Bilal", "age": 31, "city": "Karachi"}]

$ python3 main.py people.json -o people.csv
Converted 2 row(s), 3 column(s): people.json -> people.csv

$ cat people.csv
name,age,city
Ayesha,28,Lahore
Bilal,31,Karachi
```

## License

MIT — see [LICENSE](LICENSE).

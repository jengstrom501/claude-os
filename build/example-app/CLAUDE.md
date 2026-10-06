# csv2json

A tiny command-line tool that converts a CSV file to JSON. Example project showing how
a filled-in `CLAUDE.md` + `STATUS.md` pair looks. Fictional; safe to delete.

<!-- Optional. Other projects this one may read without asking, comma-separated. -->
<!-- Imports: manage/some-area -->

## How to resume
Read STATUS.md, show state + next step, wait for direction.

## Run / test
- `python csv2json.py input.csv > output.json`
- `python -m unittest`

## Hard rules
- Standard library only. No third-party dependencies.
- Never modify the input file; write results to stdout or a new file.

# Status — csv2json
**Objective:** A single-file CLI that turns any CSV with a header row into a JSON array of objects.
**Now:** 2026-03-02 — scaffolded; `csv2json.py` not written yet.
**Next:** Write `csv2json.py` with header-row parsing and a `--pretty` flag, plus a unittest for a 3-row sample.
## Decisions
- 2026-03-02 — Output is a JSON array of objects keyed by header — simplest shape for downstream tools.
- 2026-03-02 — Standard library only (`csv`, `json`, `argparse`) — keeps install to "copy one file".
## Open questions
- Should numeric-looking fields be converted to numbers, or stay strings? Default: strings.
## Assumptions
- Input is UTF-8 and the first row is a header.
## Artifacts
- `csv2json.py` — the tool (not yet created)

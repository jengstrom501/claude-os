# Build

Products, ventures, and code projects. One directory per project; `python system/projects.py`
lists them. Each project is isolated (root CLAUDE.md → Project isolation).

## Working here
- Project = `CLAUDE.md` (run/test commands, hard rules, `Imports:`) + `STATUS.md` (state, decisions).
- Default build loop (root CLAUDE.md → Orchestration): done-when criteria → `worker` builds →
  tests run → `reviewer` checks → orchestrator decides. Small fixes: just do them and run the tests.
- Heavier planning/review skill chains (if installed) are opt-in per project, for high-stakes or
  multi-session builds. A project that uses one says so in its own CLAUDE.md.

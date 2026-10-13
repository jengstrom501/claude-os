# Claude OS

A Claude Code harness for Windows. Opus orchestrates; a Sonnet `worker` executes bounded
tasks; a Haiku `scout` does cheap bulk work; a Sonnet `reviewer` checks finished work
read-only. Each project is isolated from the others, and a hook enforces it. Routing is
deterministic (a script, not a guess), and `/tune` turns a rough request into a precise
plan before anything runs.

## Quickstart

1. Clone this repo.
2. In PowerShell, from the repo root: `powershell -ExecutionPolicy Bypass -File .\setup.ps1` (checks Python and Claude Code, runs the guard's tests, prints the project index).
3. Open the folder in Claude Code (`claude` in the folder, or your editor extension).
4. Run `/hooks` and approve the project hook when prompted.
5. Try `/tune <a rough request>`.

## Layout

```
CLAUDE.md            global instructions, always loaded
TODO.md              cross-cutting tasks
LICENSE, .gitignore
setup.ps1            setup check
.claude/
  settings.json      registers the project guard and STE hooks
  agents/            worker, scout, reviewer
  skills/tune/       the /tune skill
  hooks/             project_guard.py + its tests, ste.md (STE writing mode)
system/
  projects.py        routing index: one line per project
  templates/         CLAUDE.md + STATUS.md for new projects
explore/ build/ manage/   your projects: <area>/<project>/
inbox/               unsorted input, routed later
build/example-app/   a filled-in example project
```

`explore/`, `build/`, and `manage/` are for research, building, and life/admin projects.
`setup.ps1` creates any that are missing.

## How it works

**Scopes.** Each kind of information has one home:

| Scope | Where | Loaded |
|---|---|---|
| Global instructions | `CLAUDE.md` | always |
| Global memory | Claude Code auto-memory | always; facts about you, nothing project-specific |
| Global capabilities | `.claude/`, `system/*.py`, installed skills | on demand |
| Project instructions | `<project>/CLAUDE.md` (run/test, hard rules, `Imports:`) | when routed |
| Project state + memory | `<project>/STATUS.md` | when routed |
| Project artifacts | `<project>/**` | just-in-time |
| Task context | conversation + scratchpad | discarded after the task |

**Routing.** `python system/projects.py` prints one line per project (area/name, title,
purpose). Claude matches your intent against it, announces `-> [build/my-app]`, reads that
project's `CLAUDE.md` and `STATUS.md`, and works there. Ambiguous requests get a question,
not a guess.

**Isolation.** A session works in one active project. `.claude/hooks/project_guard.py`
makes the first project a session touches the active one. After that, touching another project,
or searching across all of them, prompts you. An approved crossing is remembered for that
session. To allow a crossing permanently, add a line to the project's `CLAUDE.md`:
`Imports: manage/other-project, build/another`. Machine- or person-specific notes go in
`CLAUDE.local.md`, which Claude Code auto-loads and `.gitignore` keeps out of the repo.
The Bash/PowerShell check scans the command for project paths, so a command that reaches
another project without naming it (for example `grep -r x .` at the root) is not caught.

**STE mode.** A `SessionStart` hook loads `.claude/hooks/ste.md`, which makes Claude write
its replies in ASD-STE100 Simplified Technical English (the style of aircraft maintenance
manuals): short sentences, one meaning per word, active voice, no idioms, no contractions.
Say "stop STE" to turn it off for the session and "STE on" to turn it back on. Code,
commands, commit messages, and file contents are not affected.

**Delegation.** The orchestrator picks the lightest path: do trivial work directly, brief
one `worker` for a clear spec, use a script or `scout` for bulk mechanical work, fan out
`worker`s for research, and add a `reviewer` after non-trivial builds. Briefs follow a
fixed shape: Goal, Inputs, Constraints, Done-when, Return shape. Agents report in a
compact format (status, changes, evidence, issues). Full rules are in `CLAUDE.md`.

**State.** `STATUS.md` is a project's state and memory: objective, now/next, dated
decisions, open questions. Claude writes it back at the end of sessions that change
status or decisions, so a new session can resume from the file alone.

**`/tune`.** Routes your request to a project, reads its `CLAUDE.md` and `STATUS.md`,
and shows a tuned prompt: goal, deliverable, requirements, out of scope, assumptions,
done-when, and a tagged plan. It asks at most three questions, then runs the plan on
"go" and reports each done-when criterion with evidence.

## Creating your first project

Ask Claude ("new project: ...") or do it by hand:

```powershell
New-Item -ItemType Directory build\my-app
Copy-Item system\templates\* build\my-app\
```

Fill in `build\my-app\CLAUDE.md` (what it is, run/test commands, hard rules; at most 40
lines) and `STATUS.md` (objective, now, next). See `build/example-app/` for a filled-in
pair. Run `python system/projects.py` to confirm it appears in the index.

## Customizing

- Edit `CLAUDE.md` to change global behavior; keep it short.
- Edit `.claude/agents/*.md` to change an agent's rules, model, or return format.
- Add skills under `.claude/skills/<name>/SKILL.md`.
- Edit `.claude/hooks/ste.md` to change the writing rules, or delete the `SessionStart` entry in
  `.claude/settings.json` to drop STE mode entirely.
- Put personal or machine-specific notes in `CLAUDE.local.md` (not committed).
- Delete `build/example-app/` when you no longer need it.

## Requirements

- Windows with PowerShell
- [Claude Code](https://claude.com/claude-code)
- Python 3.8+ on PATH as `python`

## License

MIT. See `LICENSE`.

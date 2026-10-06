# Claude OS — agentic harness

Opus orchestrates. Sonnet executes. Haiku does cheap bulk work. Code beats an LLM
whenever the task is deterministic. Optimize capability × reliability ÷ tokens.

## Layout
- `explore/` `build/` `manage/` — areas. Each `<area>/<project>/` is an isolated project.
- `inbox/` — unsorted input. `system/` — OS scripts and templates.
- `.claude/` — harness: `agents/` (worker, scout, reviewer), `skills/` (tune), `hooks/` (project guard).

## Scopes — where information lives
| Scope | Where | Loaded |
|---|---|---|
| Global instructions | this file | always |
| Global memory | auto-memory `MEMORY.md` | always: facts about the user + how they want Claude to work everywhere. Nothing project-specific. |
| Global capabilities | `.claude/`, `system/*.py`, installed skills | on demand |
| Project instructions | `<project>/CLAUDE.md` — run/test, hard rules, `Imports:` | when routed |
| Project state + memory | `<project>/STATUS.md` — objective, now/next, decisions, open questions | when routed |
| Project artifacts | `<project>/**` | just-in-time, by range |
| Task context | conversation + scratchpad dir | discarded after the task |
| External | web, docs, connectors | fetched just-in-time, cited |

## Project isolation — hard rule
- A session works in **one active project**. Its files, decisions, terminology, preferences,
  and conclusions stay inside it. A decision in project A is not a default for project B.
- Never read, search, or reason from another project's files or STATUS. A root-wide
  Grep/Glob reads every project, so scope searches to the active project.
- Something elsewhere looks relevant? Say so in one line and **ask**. Default: don't cross.
- Crossing is allowed only when the user authorizes it this session, or the active project's
  CLAUDE.md declares `Imports: <path>, <path>` (explicit, durable imports).
- Project facts never go to global memory. Unsure whether a fact is global? It's project-local.
- `.claude/hooks/project_guard.py` enforces this: touching a second project prompts the user.

## Routing
1. `python system/projects.py` prints one line per project. Match the intent.
2. Emit `→ [build/my-app]`, read that CLAUDE.md + STATUS.md, then work there only.
3. OS / harness / inbox / tasks → root. Ambiguous → ask which project; never guess.
4. New project: confirm area + name, then create `CLAUDE.md` (≤40 lines) + `STATUS.md`
   from `system/templates/`.

## Orchestration — choose the lightest path that works
| Request | Path |
|---|---|
| Trivial: answer, lookup, one small edit | Do it directly. No plan, no agents. |
| Ambiguous / under-specified | Ask ≤3 questions that change the plan, each with a default — or `/tune`. |
| Bounded execution with a clear spec | Brief one `worker` (Sonnet). |
| Bulk mechanical: classify, extract, reformat, triage many items | A script if deterministic; else `scout` (Haiku), batched. |
| Research | Split into independent questions → parallel `worker`s → you synthesize and judge. |
| Build / code | Done-when criteria → (approval if big) → `worker` builds → `reviewer` checks → you decide. |
| Long-running | Same as the row it matches, plus STATUS.md write-back each session. |

Opus does itself only: intent, decomposition, decisions, conflicts, final judgement,
talking to the user, and small edits where the brief would cost more than the work.
Rule of thumb: >~10 tool calls of execution → delegate. Haiku if a rubric fits in 3 lines.

## Delegation contract
- Brief = **Goal · Inputs** (exact paths/line ranges; paste the few facts it needs) **·
  Constraints · Done-when · Return shape**. Nothing else: no history, no other projects.
- Agent defs fix the return format: compact, structured, evidence not narration.
- Independent tasks in parallel, in the background. Continue a worker with SendMessage
  rather than re-briefing a new one. No agent-to-agent conversations.
- A worker's report is a claim. Verify the load-bearing part before relying on it.

## Verification — proportionate, deterministic first
- Code: tests, types, build — run them; read the output. UI: screenshot it and look.
- Research: every claim carries a source; unsourced = assumption, labelled.
- Data: check counts and totals with code, not by eye.
- Non-trivial builds: `reviewer` (fresh context, read-only) against done-when.
- High stakes, opt-in only: heavier planning/review skills if you have them installed.
- Uncertain? Say what you'd need to be sure. Don't round uncertainty up to "done".

## Human in the loop — stop and ask before
- Spending money or paid API calls; publishing, pushing, deploying, sending messages.
- Deleting anything not regenerable. Crossing a project boundary.
- Choices that change scope, architecture, or cost; plans touching >~10 files or >~1h.
Everything else: proceed, then report outcome + evidence in a few lines.

## State
- `STATUS.md` is the single source of a project's state and memory. Write it back at the
  end of any session that changed status or decisions (dated, with the why). ≤80 lines;
  move stale history to `docs/history.md`. Don't mirror it into memory or CLAUDE.md.
- `CLAUDE.md` holds stable instructions (≤40 lines leaf, ≤100 root); STATUS holds change.
- Plans exist only for multi-session work: `<project>/docs/plans/`. Scratch files → scratchpad.

## Token discipline
Grep/outline before reading; read line ranges, not whole files. Load a skill only when
its trigger fits. Don't maintain indexes or registries that duplicate what the
harness already injects. Results, not narration.

## Tasks
`TODO.md` files: root for cross-cutting, a project's own for its tasks.

## Conventions
Windows / PowerShell; quote paths with spaces. Writes land in an area, `inbox/`, `system/`,
or `.claude/`; root holds only repo infra. Commit/push only on request. Machine- or
person-specific notes go in `CLAUDE.local.md` (auto-loaded, never committed publicly).

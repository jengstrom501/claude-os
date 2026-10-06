---
name: tune
description: Refine a rough request into a precise, outlined prompt together with the user, then execute it. Use when the user types /tune <request> or asks to "tune" a request.
argument-hint: <rough request>
---
# /tune — refine, then act

Tuning is judgement work: the orchestrator (Opus) does it, not a subagent.

## 1. Tune
1. Route the request to one project (CLAUDE.md → Routing). Tuning happens inside that
   project only.
2. Gather only the context that removes guesswork: the project's CLAUDE.md and STATUS.md,
   maybe one grep. No research yet.
3. Show the tuned prompt:

   **Goal** — the outcome, in one sentence (not the activity)
   **Project** — `area/project`
   **Deliverable** — what exists when done, and its form
   **Requirements** — bullets
   **Out of scope** — bullets
   **Assumptions** — what you inferred; each one vetoable
   **Done when** — checkable criteria
   **Plan** — 3–7 steps, each tagged `[opus]` `[sonnet]` `[haiku]` `[script]`, with ⏸ at human-approval stops

   Then ask at most 3 questions, only ones whose answer changes the plan, each with a default.
4. On the user's edits, show only the changed lines, not the whole prompt again.
   "go" (or similar) → act. "go" with questions still open → use the defaults.
   Stop tuning after two rounds; anything still open becomes a labelled assumption.

If the request is already tight (clear goal, deliverable, done-when), say
"Already tight — acting on: <goal>" and skip to Act.

## 2. Act
Treat the tuned prompt as the spec. Run it with the CLAUDE.md orchestration rules:
delegate by tag, honour ⏸ stops, verify against **Done when**. Finish with each
criterion ✓/✗ plus its evidence. If decisions changed, record them in the project's STATUS.md.

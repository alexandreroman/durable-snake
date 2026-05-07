# Project Memory

> When a new decision **contradicts** an existing
> memory note, do NOT silently override it.
> Instead: surface the conflict, quote the
> existing memory, explain how the new decision
> differs, and ask for explicit confirmation
> before updating. **Do NOT take any action** —
> no tool calls, no file writes — until confirmed.

- [Project intent and theming](references/project_overview.md) — Durable Snake is a deliberate pun on Temporal's durable-execution product; preserve the theme in future features
- [mpremote workflow with the Replay Badge](references/mpremote_workflow.md) — always use `resume`, never parallelize on the same port, retry transient "could not enter raw repl" errors
- [Folder-app game state invariants](references/game_state_invariants.md) — game-state dicts must include `last_frame: 0` before calling `DualScreenSession.frame_due`
- [Badge on-device documentation](references/badge_docs.md) — pull `/docs/API_REFERENCE.md` and `/docs/MicroPythonDeveloperGuide.md` from the badge instead of guessing APIs
- [Badge firmware updates URL](references/badge_updates.md) — https://badge.temporal.io is the official site for firmware updates and badge info

# Durable Snake

A MicroPython snake game with three retries for the
Temporal Replay Badge (ESP32-S3).

See [README.md](README.md) for full documentation.

## Tech stack

- MicroPython (firmware: 1.27.0 on Replay Badge)
- ESP32-S3 hardware (OLED 128×64, LED 8×8 matrix,
  joystick, IMU, IR, vibration motor)
- `mpremote` as the host-side deployment CLI
- Badge-side libraries: `badge` (native module),
  `badge_app`, `badge_ui` (auto-importable from
  `/lib/`)

## Build & run

There is no build step — MicroPython is copied
verbatim to the badge. Host source lives in `app/`,
on-badge target is `:apps/durable_snake/`. Deploy
and launch:

```bash
PORT=/dev/cu.usbmodem2101  # or whatever mpremote devs reports
mpremote connect "$PORT" resume cp \
    app/engine.py :apps/durable_snake/engine.py
mpremote connect "$PORT" resume cp \
    app/main.py :apps/durable_snake/main.py
# Launch from the badge's Apps menu → durable_snake
```

## Modules

- `app/main.py` — entry point that
  registers the app with `run_app(...)` and wires
  the cleanup callback.
- `app/engine.py` — game state,
  rules, OLED rendering, LED matrix rendering,
  visual effects, and screens (title, play,
  continue, game over).

## Agents

Use the following agents (from the
[skillbox](https://github.com/alexandreroman/skillbox)
plugin) for all code tasks:

- **code-writer** — for ANY task that writes,
  modifies, or refactors code. This includes
  one-line fixes, import changes, visibility
  tweaks, and adding assertions. Never use
  the Edit or Write tools directly on source
  files — always delegate to this agent.
- **code-reviewer** — for read-only code review
  before merging or when investigating issues.

## Memory

At the start of every conversation, read
`.claude/project-memory/MEMORY.md` to load
project context from previous conversations.

Use the **project-memory** skill (from the
[skillbox](https://github.com/alexandreroman/skillbox)
plugin) proactively — without being asked — whenever
the conversation reveals project decisions, deadlines,
team context, external references, workflow preferences,
or corrective feedback worth persisting across
conversations.

**Important:** Always use the **project-memory**
skill to persist information. Never use the built-in
auto-memory system (`~/.claude/projects/.../memory/`)
for project decisions or context — it is local and
not shared with the team.

## Conventions

- Line length limits for readability:
  - Text / Markdown: 80 columns max
  - Code: 120 columns max
- Follow standard Markdown conventions: blank line
  before and after headings, blank line before and
  after lists, fenced code blocks with a language tag
- Always use the latest LTS or stable version of
  languages, frameworks, and libraries. Check the
  official documentation or use available tools
  (e.g. context7) to verify current versions before
  choosing a dependency.

Badge-specific rules (mpremote workflow, on-device
docs, folder-app invariants) live in project memory
under `.claude/project-memory/`. Read `MEMORY.md`
there at the start of each session.

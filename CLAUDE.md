# Temporal Replay 2026 Badge Apps

A collection of MicroPython apps for the Temporal
Replay Badge (ESP32-S3). Each app lives in its own
folder under `apps/`.

See [README.md](README.md) for full documentation.

## Tech stack

- MicroPython (firmware: 1.27.0 on Replay Badge)
- ESP32-S3 hardware (OLED 128×64, LED 8×8 matrix,
  joystick, IMU, IR, vibration motor)
- `mpremote` as the host-side deployment CLI
- Badge-side libraries: `badge` (native module),
  `badge_app`, `badge_ui` (auto-importable from
  `/lib/`)

## Repository layout

```
apps/
├── durable_snake/             # snake game with three retries
│   ├── ds_engine.py
│   └── main.py
└── starfield_nametag/         # animated starfield + nametag text
    ├── sn_engine.py
    └── main.py
```

Each app's host-side folder under `apps/` is named
identically to its on-badge target so the same path
string works on both sides
(`apps/durable_snake/` → `/apps/durable_snake/`).
Folder names use underscores because Python modules
cannot contain hyphens. Each `main.py` must set
`APP_DIR` to the full on-badge path
(`/apps/<folder>`) — never `/app` or any
abbreviated form.

## Build & run

There is no build step — MicroPython is copied
verbatim to the badge. Deploy and launch:

```bash
PORT=/dev/cu.usbmodem2101  # whatever mpremote devs reports
APP=durable_snake          # or starfield_nametag

for f in apps/$APP/*.py; do
    mpremote connect "$PORT" resume cp "$f" ":apps/$APP/$(basename "$f")"
done
# Hard-reset the badge, then launch from the Apps menu.
```

## Apps

- **`apps/durable_snake/`** — snake game with three
  retries, a deliberate pun on Temporal's
  durable-execution product. Per-app docs live in
  the folder.
- **`apps/starfield_nametag/`** — animated
  perspective starfield with a configurable
  centered text overlay (nametag / event tagline).
  Optional JSON config on the badge at
  `/starfield_nametag_config.json`.

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

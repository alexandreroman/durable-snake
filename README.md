# Temporal Replay 2026 Badge Apps

A collection of MicroPython apps for the **Temporal
Replay Badge** (ESP32-S3) handed out at Temporal
Replay 2026 — ambient displays, games, and other
small experiences that run on the badge's OLED, 8×8
LED matrix, and joystick.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

## Apps

| App                                          | What it is                                                                        |
| -------------------------------------------- | --------------------------------------------------------------------------------- |
| [durable_snake](apps/durable_snake/)         | Snake game with three retries — a play on Temporal's *durable execution* product. |
| [starfield_nametag](apps/starfield_nametag/) | Animated starfield with a centered nametag — personalized from `/badgeInfo.json`. |

Each app lives in its own folder under `apps/`, with
its source under `apps/<name>/` and a per-app README
covering controls, configuration, and architecture.

## Prerequisites

- A **Temporal Replay Badge** (ESP32-S3) running
  MicroPython 1.27.0 or later, connected over USB.
- **`mpremote`** 1.27.0 or later on your host
  machine (`brew install mpremote` or
  `pipx install mpremote`).
- The badge's standard libraries (`badge`,
  `badge_app`, `badge_ui`) — pre-installed on
  Temporal-issued badges.

## Deploying an app

There is no build step — MicroPython is copied
verbatim to the badge. Each app's host-side folder
under `apps/` is named identically to its on-badge
target (e.g. `apps/durable_snake/` →
`/apps/durable_snake/`), so the same path string
works on both sides. Folder names use underscores
because Python modules cannot contain hyphens.

```bash
# Find the badge's serial port
mpremote devs

# Pick the app you want to deploy
PORT=/dev/cu.usbmodem2101
APP=durable_snake          # or starfield_nametag

mpremote connect "$PORT" resume mkdir ":apps/$APP"
# Each app's engine is named with an app-specific prefix
# (ds_engine.py / sn_engine.py) — see the per-app README.
for f in apps/$APP/*.py; do
    mpremote connect "$PORT" resume cp "$f" ":apps/$APP/$(basename "$f")"
done
```

> **Note** — always use `resume` with this badge.
> The firmware does not emit `soft reboot` after
> Ctrl-D, so the default `mpremote connect ...` mode
> fails to enter raw REPL.

After deploying, **hard-reset the badge** before
launching the app, otherwise the cached module
from the previous run will execute. Launch the app
from the badge's **Apps** menu.

## Repository layout

```
.
├── apps/
│   ├── durable_snake/         # snake game
│   │   ├── ds_engine.py
│   │   └── main.py
│   └── starfield_nametag/     # ambient starfield + nametag
│       ├── sn_engine.py
│       └── main.py
├── CLAUDE.md                  # Claude Code project rules
├── LICENSE
└── README.md
```

## Firmware and badge info

The official site for badge firmware updates and
hardware info is [badge.temporal.io](https://badge.temporal.io).

## Contributing

Bug reports and small patches are welcome through
GitHub issues and pull requests. Match the existing
code style (no decorative comments, short
docstrings, descriptive identifiers over prose).

## License

This project is licensed under the Apache-2.0
License — see [LICENSE](LICENSE) for details.

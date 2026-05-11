---
name: "Project intent and theming"
description: "Temporal Replay 2026 Badge Apps is a multi-app MicroPython repo for the Replay Badge; preserve each app's distinct theme"
type: project
---

# Project intent and theming

`temporal-replay-badge-apps` is a collection of
MicroPython apps for the Temporal "Replay Badge"
(ESP32-S3), distributed at **Temporal Replay 2026**.
The repo is structured as one folder per app under
`apps/`, sharing a common deploy workflow
(`mpremote ... resume cp`) and the badge's standard
libraries (`badge`, `badge_app`, `badge_ui`).

The repo grew out of two earlier single-app repos
(`durable-snake` and `temporal-replay-starfield`)
which were merged in May 2026. Each app keeps its
own theme:

- **`apps/durable_snake/`** — Snake game with three
  retries. Name is a deliberate pun on Temporal's
  *durable execution* product: retries restart the
  snake fresh but preserve the score, mirroring how
  a Temporal workflow keeps its durable state across
  replays.
- **`apps/starfield_nametag/`** — Ambient
  perspective starfield on the OLED with a
  configurable centered text (intended as a
  conference nametag / event tagline like
  "Replay 2026"). The 8×8 LED matrix mirrors the
  effect with smaller drifting stars. Not a game —
  pure ambient display.

**Why:** The badge work doubles as developer
advocacy / demo material for Temporal Replay 2026.
The apps are meant to be visible on attendees' desks
and lanyards; theming is part of the product, not a
coincidence.

**How to apply:** When the user asks for new
features in an app, prefer extensions that
reinforce *that* app's theme — for `durable_snake`,
extensions reinforcing the durable-execution
metaphor (checkpoints, replays, retry policies,
workflow-style framing); for `starfield_nametag`,
extensions reinforcing space / motion / typography
(projection modes, LED color schemes, multi-line
or scrolling text, configurable star density).
When the user asks for a *new* app, treat it as a
new folder under `apps/` with its own theme — do
not collapse apps together or pull one toward the
mechanics of another.

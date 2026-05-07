---
name: "Badge on-device documentation"
description: "Authoritative API and developer docs are stored on the badge filesystem under /docs/, pull them with mpremote rather than guessing"
type: reference
---

# Badge on-device documentation

The Temporal Replay Badge ships with its own
authoritative documentation on flash:

- `/docs/API_REFERENCE.md` (~39 KB) — full reference
  for every function in the `badge` native module,
  plus `badge_app` and `badge_ui` helpers.
- `/docs/MicroPythonDeveloperGuide.md` (~29 KB) —
  developer guide for writing apps on the badge.
- `/docs/README.md` — index.

When in doubt about an API signature, semantics, or
constant, pull the relevant file with
`mpremote ... resume cp :docs/<file>.md .` instead
of guessing from training data — the firmware ships
custom Temporal-flavored APIs that aren't in
upstream MicroPython docs.

The badge filesystem also contains canonical app
examples under `/apps/` (e.g.
`/apps/breaksnake/`) that demonstrate the
folder-based app pattern with full chrome, score
persistence, and dual-screen rendering.

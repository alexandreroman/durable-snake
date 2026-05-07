---
name: "Project intent and theming"
description: "Durable Snake is a Temporal-themed snake variant; the name is a deliberate pun on Temporal's durable-execution product"
type: project
---

# Project intent and theming

Durable Snake is a MicroPython app for the
Temporal "Replay Badge" (ESP32-S3). The name is an
intentional play on Temporal's *durable execution*
product positioning — the snake survives bites
because each run is "durable" (3 retries continue
at the same speed and same score).

**Why:** The badge work doubles as developer
advocacy / demo material for Temporal. The theme
is part of the product, not a coincidence.

**How to apply:** When the user asks for new
features or alternate modes, prefer extensions
that reinforce the durable-execution metaphor
(e.g. saved checkpoints, replays, retry policies,
"workflow"-style framing) over removing the retry
mechanic, renaming the app, or pulling the design
toward a generic snake.

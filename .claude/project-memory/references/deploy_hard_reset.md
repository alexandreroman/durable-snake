---
name: "Hard reset required after each app deployment"
description: "After copying updated app files to the badge, a hard reset is required before the new code takes effect"
type: feedback
---

# Hard reset required after each app deployment

After deploying updated app files to the badge
(e.g. `mpremote ... cp app/engine.py
:apps/durable_snake/engine.py`), the badge must be
hard-reset before the changes are visible when
launching the app.

**Why:** The badge keeps the previously-loaded app
modules in memory. Re-launching the app from the
Apps menu reuses the cached modules, so newly
copied source files are not picked up until the
firmware boots fresh.

**How to apply:** After every `mpremote ... cp`
that touches an app source file, ask the user to
physically hard-reset the badge (power cycle or
reset button) before verifying the change. Do not
suggest software-triggered resets — the user
prefers a real hardware reset.

Do not assume a soft reload is enough — re-opening
the app from the menu will run the stale cached
version and waste a debugging cycle.

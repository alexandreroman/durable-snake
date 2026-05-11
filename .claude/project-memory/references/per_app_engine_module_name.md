---
name: "Per-app engine module must have a unique name"
description: "Each folder-app's engine module must use an app-specific name (e.g. ds_engine, sn_engine), not the generic `engine`, to avoid sys.modules cache collisions on MicroPython"
type: project
---

# Per-app engine module must have a unique name

Each folder-app under `apps/<name>/` must name its
engine module with a short app-specific prefix
(e.g. `ds_engine.py` for `durable_snake`,
`sn_engine.py` for `starfield_nametag`). The
matching `main.py` imports from that name:
`from ds_engine import main, cleanup`. Never use
the generic name `engine.py`.

**Why:** MicroPython caches imported modules in
`sys.modules` by name. Once any app loads a module
called `engine`, every other app's
`from engine import …` returns the cached version
from the wrong app and crashes on the badge. The
canonical badge example `breaksnake` follows the
same convention with `bs_engine.py` for exactly
this reason.

**How to apply:** When creating a new folder-app
or reviewing one, ensure the engine module file
is named `<prefix>_engine.py` and that `main.py`
imports from that exact name. If `starfield_nametag`-
style code needs to keep using a local
`engine.<attr>` alias (e.g. `engine.set_text(...)`),
import with `import sn_engine as engine` rather
than renaming back to the colliding generic name.

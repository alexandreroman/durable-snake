---
name: "MicroPython math.hypot is missing on the Replay Badge"
description: "The badge's MicroPython math module omits hypot; use math.sqrt(a*a + b*b) instead"
type: feedback
---

# MicroPython math.hypot is missing on the Replay Badge

The Replay Badge's MicroPython `math` module
does NOT provide `math.hypot`. Calling it
raises:

```
AttributeError: 'module' object has no attribute 'hypot'
```

at module import time, which surfaces as a hard
crash on launch.

```python
# Wrong — crashes on the badge:
MAX_RADIUS = math.hypot(OLED_W, OLED_H) / 2

# Correct:
MAX_RADIUS = math.sqrt(OLED_W * OLED_W + OLED_H * OLED_H) / 2
```

**Why:** Reproduced live with
`mpremote ... resume exec "import engine"` —
the badge's MicroPython port omits some
optional `math` helpers. Confirmed available:
`math.sqrt`, `math.pi`, `math.sin`, `math.cos`,
`math.atan2`. Confirmed missing: `math.hypot`.
Other CPython-only helpers (`math.dist`,
`math.tau`, `math.inf`, `math.nan`) are likely
also absent.

**How to apply:** Avoid `math.hypot` in any
code targeting the badge — replace with
`math.sqrt(a*a + b*b)`. Before relying on any
non-trivial `math.<name>` symbol, either check
`/docs/API_REFERENCE.md` or quickly probe with
`mpremote ... resume exec "import math; print(dir(math))"`.
This applies to MicroPython generally, but the
crash mode (silent at host syntax-check time,
loud only at on-device import) makes it
specifically worth flagging for badge work.

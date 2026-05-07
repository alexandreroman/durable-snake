---
name: "Folder-app game state invariants"
description: "Game-state dicts passed to badge_app helpers must include last_frame: 0 to avoid KeyError in DualScreenSession.frame_due"
type: feedback
---

# Folder-app game state invariants

When writing a folder app (`/apps/<name>/main.py`
+ supporting modules) for the Temporal Replay
Badge, the game-state dict you pass into
`DualScreenSession.frame_due(game, now)` must
contain a `"last_frame"` key initialized to `0`.

```python
def new_game():
    return {
        ...,
        "last_frame": 0,    # required by DualScreenSession.frame_due
    }
```

**Why:** `frame_due` reads `game[key]` (default key
`"last_frame"`) directly with no default, so a
missing key raises `KeyError` on the first frame
tick. The error surfaces as a generic crash report
on the badge, which is misleading because the rest
of the game state looks correct.

**How to apply:** When initializing any new
folder-app game state, include `"last_frame": 0`
in the dict. If you also use multiple frame
cadences via the `key` parameter (e.g.
`frame_due(game, now, key="led_frame")`),
initialize each one to `0` as well.

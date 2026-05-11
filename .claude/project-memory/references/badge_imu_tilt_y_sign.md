---
name: "Badge IMU tilt_y sign disagrees with dev guide"
description: "On this Replay Badge, imu_tilt_y() is positive when the OLED-end points down (lanyard); sign is reversed vs the dev guide, and imu_face_down() does NOT fire in lanyard mode despite the guide's example."
type: project
---

# Badge IMU tilt_y sign disagrees with dev guide

`imu_tilt_y()` on the Temporal Replay Badge returns
values with the **opposite sign** to what the
on-device `MicroPythonDeveloperGuide.md` documents.

Measured empirically (2026-05-11) on the actual
hardware:

- Held in hand, badge near-flat, OLED visible:
  `imu_tilt_y()` ≈ **-75 mG**
- Hanging on a lanyard, OLED-end pointing down,
  badge vertical: `imu_tilt_y()` ≈ **+950 mG**

The dev guide claims negative tilt_y means "tilted
toward upside-down". Direct measurement contradicts
this: lanyard / upside-down orientation produces a
strongly **positive** tilt_y.

**Why:** lanyard-flip detection in
`apps/starfield_nametag/sn_engine.py` was originally
written from the dev guide and never triggered on
the real badge. Trust the measurement over the doc.

**How to apply:** When writing orientation logic
that consumes `imu_tilt_y()`, use positive
thresholds for "upside-down / lanyard" detection
(e.g. enter at +500 mG, exit at +300 mG with
hysteresis). Do not copy sign conventions from
`/docs/MicroPythonDeveloperGuide.md` without
re-measuring. If `imu_tilt_x()` or `imu_tilt_z()`
matters for a feature, measure those independently
too — the guide may be wrong about them as well.

## Don't use `imu_face_down()` for lanyard detection

The on-device
`/docs/MicroPythonDeveloperGuide.md` example wires
nametag/lanyard detection to `imu_face_down()`:

```python
if imu_face_down():
    oled_println("Walking mode!")
```

This is misleading. `imu_face_down()` thresholds
on the **Z-axis** — it only returns `True` when
the screen is physically pointing toward the
floor (e.g. badge laid screen-down on a table).
It does **not** fire when the badge hangs
vertically on a lanyard, because in that posture
the OLED faces roughly horizontally and Z is near
zero.

Measured during the same 2026-05-11 session,
`imu_face_down()` stayed `False` in every
real-use orientation the user tested:

- Held in hand, OLED visible: `False`
- Hanging on a lanyard around the neck: `False`
- Flat on the desk, OLED up: `False`
- Tilted, swung, in motion: `False`

It only goes `True` if you deliberately flip the
badge so the OLED points at the floor — which is
not a normal wearing or holding posture.

**How to apply:** Use `imu_tilt_y()` for
lanyard/nametag detection (see thresholds above).
Reserve `imu_face_down()` for the literal
"screen-on-table" case, e.g. a privacy or
sleep-while-face-down feature. If you read the
dev guide example and assume it works, the app
will silently never trigger — that exact bug
ate hours during the starfield_nametag IMU work.

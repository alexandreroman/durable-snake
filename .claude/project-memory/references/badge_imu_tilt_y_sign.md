---
name: "Badge IMU tilt_y sign disagrees with dev guide"
description: "On this Replay Badge, imu_tilt_y() is positive when the OLED-end points down (lanyard); the dev guide's sign convention is reversed."
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

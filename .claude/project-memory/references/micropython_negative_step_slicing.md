---
name: "MicroPython does not support negative-step slicing"
description: "MicroPython on the Replay Badge rejects s[::-1] and any slice with step != 1 at runtime"
type: project
---

# MicroPython does not support negative-step slicing

MicroPython on the Replay Badge (firmware 1.27.0)
raises `NotImplementedError: only slices with
step=1 (aka None) are supported` for any slice
expression with a step other than `1`/`None`,
including the common `s[::-1]` reverse idiom.
CPython accepts it; MicroPython does not.

**Why:** Bit Encountered while implementing the
180° framebuffer rotation in
`apps/starfield_nametag/sn_engine.py`: the
`_BIT_REVERSE` lookup table was built with
`int("{:08b}".format(i)[::-1], 2)`, which compiles
fine but crashes at module import on the badge.

**How to apply:** When writing or reviewing code
that runs on the badge, never use `s[::-1]` or any
`a:b:step` slice with `step != 1`. To reverse a
sequence, use an explicit loop, `reversed(...)`,
or arithmetic (for bit-reversal, the three
swap-shift steps on `0xF0/0x0F`, `0xCC/0x33`,
`0xAA/0x55`). The badge's `dir()` and on-device
docs will not flag this — it only surfaces at
runtime.

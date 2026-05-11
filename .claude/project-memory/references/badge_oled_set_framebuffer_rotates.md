---
name: "Badge oled_set_framebuffer() applies a hidden 180° rotation"
description: "Replay Badge firmware quirk: oled_set_framebuffer() is not the inverse of oled_get_framebuffer(); it rotates input by 180° before storing."
type: reference
---

# Badge oled_set_framebuffer() applies a hidden 180° rotation

On the Temporal Replay 2026 badge (MicroPython
firmware 1.27.0), `oled_set_framebuffer(data)` is
**not** the symmetric inverse of
`oled_get_framebuffer()`. Verified empirically on
hardware:

- `oled_get_framebuffer()` returns 1024 bytes in
  standard SSD1306 vertical-byte layout: byte
  `i = p*128 + c` covers (col=c, page=p, rows
  `p*8..p*8+7`); LSB = top pixel.
- `oled_set_framebuffer(data)` stores
  `internal[1023 - i] = bit_reverse(data[i])`.
  That is: page-flip + column-flip + per-byte
  bit-reverse — algebraically equivalent to a
  180° rotation of the input before storing.

**Net effect:** doing a manual 180° rotation in
software and then calling `set_framebuffer`
double-flips → identity (no visible change).

**The shortcut:**

```python
oled_set_framebuffer(oled_get_framebuffer())
```

flips the display 180° in one call. Confirmed
end-to-end: a pixel set at (0, 0) before the call
ends up at (127, 63) after; (10, 5) ends up at
(117, 58).

## Why this matters

The badge's on-device docs
(`/docs/API_REFERENCE.md`,
`/docs/MicroPythonDeveloperGuide.md`) do not
mention this asymmetry. Any future code that
calls `oled_set_framebuffer` with a hand-built
or manually transformed buffer will be silently
wrong unless it accounts for the firmware's
internal rotation.

## How to apply

- To rotate the OLED 180° (e.g. for lanyard /
  upside-down mode): use the one-liner above
  instead of writing pixel-by-pixel or page-by-page
  rotation code. See `_rotate_fb_180()` in
  `apps/starfield_nametag/sn_engine.py`.
- If you ever need to write an externally-prepared
  framebuffer verbatim, pre-rotate it 180° and
  bit-reverse each byte so the firmware's hidden
  transform inverts back to the intended layout.
- Do NOT "fix" the one-liner by adding manual
  rotation logic — that doubles the flip into a
  no-op, which is exactly the bug that prompted
  this note.

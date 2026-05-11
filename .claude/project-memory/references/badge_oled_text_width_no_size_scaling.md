---
name: "Badge oled_text_width does not scale linearly with text size"
description: "Badge default font is Spleen 9px; oled_text_width returns real rendered widths but they don't follow chars*6*size — always probe via the firmware function"
type: reference
---

# Badge oled_text_width does not scale linearly with text size

The Replay Badge MicroPython firmware (1.27.0)
ships with the default font set to **"Spleen 9px"**
(verify with `oled_get_current_font()`). For this
font, `oled_text_width(text)` returns the actual
on-screen rendered width, but the width does **not**
scale linearly with `oled_set_text_size(s)` and does
**not** follow the standard Adafruit GFX formula
`width = chars * 6 * size`.

Measured on hardware for `"Hi, I'm Alexandre!"`
(18 chars):

| `oled_set_text_size(s)` | `oled_text_width(...)` |
|---|---|
| 1 | 70  |
| 2 | 90  |
| 3 | 90  |
| 4 | 108 |

Sizes 2 and 3 collapse to the same width, and the
overall progression is far below `18 * 6 * size`.

## How to apply

When auto-fitting a string into a horizontal
budget on the OLED, **trust the firmware**:

```python
for size in (4, 3, 2, 1):
    oled_set_text_size(size)
    if oled_text_width(text) <= budget:
        chosen = size
        break
oled_set_text_size(1)  # restore to leave global
                       # text-size state predictable
```

Do **not** compute widths arithmetically — any
formula based on character count and `size` will
be wrong for the default Spleen 9px font (and
probably for every other non-`5x7` font listed by
`oled_get_fonts()`).

If you want predictable `chars * 6 * size`
geometry, explicitly switch to the `5x7` font via
`oled_set_font("5x7")` first — otherwise assume
the active font is non-standard.

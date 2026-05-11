# Project Memory

> When a new decision **contradicts** an existing
> memory note, do NOT silently override it.
> Instead: surface the conflict, quote the
> existing memory, explain how the new decision
> differs, and ask for explicit confirmation
> before updating. **Do NOT take any action** —
> no tool calls, no file writes — until confirmed.

- [Project intent and theming](references/project_overview.md) — multi-app repo for Temporal Replay 2026 (durable_snake, starfield_nametag, …); preserve each app's distinct theme
- [mpremote workflow with the Replay Badge](references/mpremote_workflow.md) — always use `resume`, never parallelize on the same port, retry transient "could not enter raw repl" errors
- [Folder-app game state invariants](references/game_state_invariants.md) — game-state dicts must include `last_frame: 0` before calling `DualScreenSession.frame_due`
- [Folder-app APP_DIR must be the full path](references/folder_app_app_dir.md) — `APP_DIR` in a folder-app `main.py` must equal `/apps/<folder>`; `/app` or other abbreviations cause `ImportError: no module named 'engine'`
- [Badge on-device documentation](references/badge_docs.md) — pull `/docs/API_REFERENCE.md` and `/docs/MicroPythonDeveloperGuide.md` from the badge instead of guessing APIs
- [Badge firmware updates URL](references/badge_updates.md) — https://badge.temporal.io is the official site for firmware updates and badge info
- [Hard reset required after each app deployment](references/deploy_hard_reset.md) — after copying updated app files, hard-reset the badge before re-launching, otherwise cached modules run
- [mpremote ls trailing-slash quirk](references/mpremote_ls_quirk.md) — `mpremote ... resume ls :path/` returns `Invalid argument`; drop the trailing slash
- [Badge serial port enumeration](references/badge_serial_port.md) — Replay Badge shows up as `/dev/cu.usbmodem2101` (VID:PID `303a:1001`); always re-check via `mpremote devs`
- [MicroPython math.hypot missing on badge](references/micropython_math_hypot_missing.md) — badge's `math` lacks `hypot`; replace with `math.sqrt(a*a + b*b)`; probe `dir(math)` before using non-trivial helpers
- [Per-app engine module must have a unique name](references/per_app_engine_module_name.md) — name each folder-app's engine `<prefix>_engine.py` (e.g. `ds_engine`, `sn_engine`) to avoid `sys.modules` collisions across apps
- [MicroPython negative-step slicing unsupported](references/micropython_negative_step_slicing.md) — `s[::-1]` and any `step != 1` slice raise `NotImplementedError` at runtime on the badge; reverse via loop/`reversed()`/arithmetic
- [Badge IMU tilt_y sign + imu_face_down caveat](references/badge_imu_tilt_y_sign.md) — measured: held ≈ -75, lanyard ≈ +950 mG (positive = upside-down, opposite of dev guide); `imu_face_down()` is Z-only and never fires on a lanyard
- [Badge oled_set_framebuffer applies a hidden 180° rotation](references/badge_oled_set_framebuffer_rotates.md) — firmware stores `internal[1023-i] = bit_reverse(input[i])`; `set_fb(get_fb())` flips display 180° in one call
- [Badge oled_text_width does not scale linearly with text size](references/badge_oled_text_width_no_size_scaling.md) — default font is Spleen 9px; trust the firmware `oled_text_width()` for auto-fit, never compute `chars*6*size`

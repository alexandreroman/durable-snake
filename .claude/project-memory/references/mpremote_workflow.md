---
name: "mpremote workflow with the Replay Badge"
description: "Three non-obvious mpremote rules for this badge: always use resume, never parallelize on the same port, retry transient raw-REPL errors"
type: feedback
---

# mpremote workflow with the Replay Badge

Three rules learned the hard way when driving the
Temporal Replay Badge from the host with mpremote.

## 1. Always use `resume`

Wrap every mpremote subcommand with `resume`:

```bash
mpremote connect <port> resume <ls|cp|exec|mkdir|rm|rmdir|...>
```

**Why:** The Replay Badge firmware does not emit
`soft reboot\r\n` after receiving the `Ctrl-D` byte
that mpremote sends as part of its default raw-REPL
handshake. The host then raises
`TransportError: could not enter raw repl` even
though the badge accepted the prompt. The `resume`
subcommand uses
`enter_raw_repl(soft_reset=False)`, which skips the
problematic step.

**How to apply:** Treat the bare
`mpremote connect <port> <cmd>` form as broken on
this hardware. Always insert `resume` before the
subcommand. This applies to one-shot commands and
to the longer `+`-chained command form.

## 2. Never parallelize on the same serial port

Do not issue two mpremote calls concurrently against
the same `/dev/cu.usbmodem*` device.

**Why:** They collide on the serial port; one of
the two will fail partway through and may leave the
badge's REPL in a half-state.

**How to apply:** Sequence every mpremote call. If
batching, chain with `&&` in a single shell command
so the subsequent calls only run after the previous
one succeeds. When using the multi-tool-call shape
of an agent, do not put two mpremote calls in the
same parallel batch.

## 3. Treat transient "could not enter raw repl"
   as retryable

If `mpremote ... resume <cmd>` fails with
`TransportError: could not enter raw repl` even
though a previous command worked, simply retry the
exact same command.

**Why:** The currently-running app on the badge
sometimes restarts between two host calls (e.g.
the boop screen). If the next mpremote call lands
during that re-init window, the badge isn't ready
to enter raw-REPL yet. By the time you retry, it's
back to a steady state.

**How to apply:** First failure: retry verbatim.
Don't change strategy, don't add sleeps, don't
swap to `--no-soft-reset`. The retry almost always
succeeds. Only investigate further if a third
consecutive attempt fails.

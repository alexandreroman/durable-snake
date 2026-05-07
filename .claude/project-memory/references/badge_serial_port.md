---
name: "Badge serial port enumeration"
description: "The Replay Badge typically enumerates as /dev/cu.usbmodem2101 on this user's macOS host; verify via mpremote devs"
type: reference
---

# Badge serial port enumeration

On this developer's macOS host, the Temporal
Replay Badge enumerates as:

```
/dev/cu.usbmodem2101  Espressif USB JTAG/serial debug unit (303a:1001)
```

**How to find it:** Run `mpremote devs` and pick
the entry whose VID:PID is `303a:1001` and whose
description contains
`Espressif USB JTAG/serial debug unit`. That row's
first column is the port path to pass to
`mpremote connect <port>`.

**Caveat:** The exact `usbmodem<N>` suffix is not
stable — macOS reassigns it based on the USB
hub/port, cable, and reboot history. Always run
`mpremote devs` at the start of a deployment
session and read the actual path; do not hardcode
`/dev/cu.usbmodem2101` in scripts. The other
`/dev/cu.*` entries on this host (Bluetooth,
debug-console, audio peripherals) are not the
badge and will fail the connect.

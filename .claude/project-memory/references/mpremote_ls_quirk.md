---
name: "mpremote ls trailing-slash quirk"
description: "mpremote 1.27.0 ls command rejects badge paths that end with a trailing slash"
type: feedback
---

# mpremote ls trailing-slash quirk

When listing a directory on the badge with
`mpremote ... resume ls`, do **not** end the path
with a trailing slash.

```bash
# Fails:
mpremote connect <port> resume ls :apps/<app>/
# -> mpremote: ls: apps/<app>/: Invalid argument.

# Works:
mpremote connect <port> resume ls :apps/<app>
```

**Why:** Reproduced live on mpremote 1.27.0 against
the Replay Badge: the trailing-slash form returns
`Invalid argument` once the raw-REPL session is
established. The no-slash form lists the directory
as expected. This is mpremote's argument parser,
not a transient REPL transport error — retrying
verbatim does not help.

**How to apply:** Strip the trailing slash from
any `:path/` argument passed to
`mpremote ... resume ls`. This applies only to
`ls`; `cp` paths can include a directory target
with or without a slash. If you see
`Invalid argument` from `ls`, check the slash
first before treating it as a transport problem.

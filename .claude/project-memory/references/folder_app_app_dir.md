---
name: "Folder-app APP_DIR must be the full /apps/<name> path"
description: "In a folder-app main.py, APP_DIR must equal the full on-badge /apps/<folder> path; shortened forms like /app cause ImportError"
type: feedback
---

# Folder-app APP_DIR must be the full /apps/<name> path

In a folder-app's `main.py`, the `APP_DIR`
constant used to extend `sys.path` MUST be the
full on-badge path (e.g.
`/apps/temporal_replay_starfield`), NOT a
shortened name like `/app`.

```python
# Correct — full on-badge path:
APP_DIR = "/apps/temporal_replay_starfield"

# Wrong — causes ImportError: no module named 'engine':
APP_DIR = "/app"
```

**Why:** The badge filesystem stores folder apps
under `/apps/<folder>/`, and the engine modules
live next to `main.py` inside that directory.
`/app` is not a real path on the badge, so the
`sys.path.insert(0, APP_DIR)` line is a no-op
and `import engine` fails. The on-device
`/docs/API_REFERENCE.md` shows
`APP_DIR = "/apps/my_app"` and the canonical
example `/apps/breaksnake/main.py` follows the
same pattern. Reproduced live: an inherited
`APP_DIR = "/app"` from earlier code crashed
the new app at launch with
`ImportError: no module named 'engine'`.

**How to apply:** When writing or reviewing a
folder-app `main.py`, always check that
`APP_DIR` matches the full deploy target
exactly: `/apps/<same folder name used with
mpremote cp>`. Never use `/app` or any other
abbreviated form, even if you find one in
existing code in the repo. If you copy `main.py`
between apps, update this constant first.

"""Frozen-app entry point for DeepTutor.app.

The PyInstaller binary is not a Python interpreter, so every internal
respawn shaped like ``sys.executable -m <module> [args...]`` (detached
launcher worker, the ``-m uvicorn`` backend, isolated document workers,
update restart) would fail with ``No such option: -m`` unless the entry
script re-implements the interpreter's module dispatch.

Launched with no arguments (a double-click in Finder) the bundle must not
print CLI help and exit, so it defaults to
``start --detach --open-browser --home <user data dir>``. A Finder launch
has cwd ``/``, so the runtime home has to be resolved here: an empty
``/data`` would leave DeepTutor running with no LLM pool configured.

The runtime home prefers an existing checkout's ``data`` dir next to the
bundle, then ``~/Library/Application Support/DeepTutor``, and falls back
to a fresh directory seeded from the settings shipped in the bundle.

Explicit arguments are passed through to the CLI unchanged.
"""

import json
import os
import runpy
import sys
from pathlib import Path


def _bundled_root() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))


def _pick_runtime_home() -> Path | None:
    root = _bundled_root()
    candidates = [
        root.parent.parent / "data",  # repo checkout next to the .app
        Path.home() / "Library" / "Application Support" / "DeepTutor",
    ]
    for candidate in candidates:
        if (candidate / "user" / "settings" / "model_catalog.json").is_file():
            return candidate
    return None


def _is_seedable(source: Path, destination: Path) -> bool:
    """Ship the pool when the target is missing or still an empty template."""
    if not destination.exists():
        return True
    try:
        payload = json.loads(destination.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return not payload.get("connections") and not payload.get("services")


def _seed_settings(home: Path) -> None:
    """Copy the shipped LLM pool into a fresh runtime home."""
    import shutil

    bundled = _bundled_root() / "packaging" / "default-settings"
    # Runtime data lives below <home>/data, not directly in <home>.
    target = home / "data" / "user" / "settings"
    target.mkdir(parents=True, exist_ok=True)
    for source in bundled.glob("*.json"):
        destination = target / source.name
        if not _is_seedable(source, destination):
            continue
        shutil.copy2(source, destination)


if len(sys.argv) >= 3 and sys.argv[1] == "-m":
    module_name = sys.argv[2]
    sys.argv = [sys.argv[0], *sys.argv[3:]]
    runpy.run_module(module_name, run_name="__main__", alter_sys=False)
else:
    if len(sys.argv) == 1:
        home = _pick_runtime_home()
        if home is None:
            home = Path.home() / "Library" / "Application Support" / "DeepTutor"
            _seed_settings(home)
        home.mkdir(parents=True, exist_ok=True)
        # The CLI configures logging at import time and resolves its home from
        # cwd (``/`` for a Finder launch), so pin it before importing anything.
        os.environ["DEEPTUTOR_HOME"] = str(home)
        sys.argv = [
            sys.argv[0],
            "start",
            "--detach",
            "--open-browser",
            "--home",
            str(home),
        ]
    from deeptutor_cli.main import main

    main()

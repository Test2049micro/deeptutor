"""Frozen-app entry point for DeepTutor.app.

The PyInstaller binary is not a Python interpreter, so every internal
respawn shaped like ``sys.executable -m <module> [args...]`` (detached
launcher worker, the ``-m uvicorn`` backend, isolated document workers,
update restart) would fail with ``No such option: -m`` unless the entry
script re-implements the interpreter's module dispatch.

Direct invocations (``DeepTutor start --detach``) fall through to the CLI.
"""

import runpy
import sys

if len(sys.argv) >= 3 and sys.argv[1] == "-m":
    module_name = sys.argv[2]
    sys.argv = [sys.argv[0], *sys.argv[3:]]
    runpy.run_module(module_name, run_name="__main__", alter_sys=False)
else:
    from deeptutor_cli.main import main

    main()

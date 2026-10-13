# DeepTutor.app packaging

This folder contains the local launcher used to build `DeepTutor.app`.

## Files
- `launcher` — bash script executed by the macOS app bundle (`exec deeptutor start --detach --open-browser`).
- `DeepTutor.app.sh` — helper to launch the app from the repo.

## Build with PyInstaller

```bash
cd /path/to/deeptutor
pip install pyinstaller
pyinstaller packaging/DeepTutor.spec
```

The output will be in `dist/DeepTutor.app`.

# DeepTutor

An agent-native intelligent learning companion with multi-agent collaboration and RAG.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[cli]"
deeptutor init --cli
```

## Run

```bash
deeptutor chat
deeptutor run deep_research "Transformer 最新进展" -l zh
deeptutor run meta_analysis "LLM tutoring effect" -l zh
```

## macOS App Bundle

A prepackaged `DeepTutor.app` is available under `packaging/`.
It is signed **ad-hoc** (`codesign --sign -`), which removes the macOS "damaged" warning.
Gatekeeper will still show **"unverified developer"** on first open; right-click the app → **Open** to bypass.
For distribution outside your own Mac, you need a **Developer ID Application** certificate + notarization.

## License

Apache-2.0. See `LICENSE`.

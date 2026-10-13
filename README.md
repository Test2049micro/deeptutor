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

A prepackaged `DeepTutor.app` is built under `dist/` by PyInstaller.
It is signed ad-hoc with the local PhotoToCodex identity, which avoids the
macOS "damaged" warning, but Gatekeeper will still show **"unverified developer"**
on first open; right-click the app → **Open** to bypass.
For distribution outside your own Mac, you need a **Developer ID Application**
certificate + notarization.

The bundled app includes the full Next.js frontend, the new cat-face app icon,
and the frozen-app launcher fixes so `start --detach` works from the `.app`.

On first launch the app seeds its runtime home
(`~/Library/Application Support/DeepTutor`) with the LLM pool config from
`packaging/default-settings/`, so it comes up with a working provider
instead of an empty catalog. Only placeholder keys ship in the bundle;
real credentials stay in your local provider service.

## License

Apache-2.0. See `LICENSE`.

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

## License

Apache-2.0. See `LICENSE`.

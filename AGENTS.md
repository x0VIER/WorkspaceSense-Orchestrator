# AI Agent Guidelines

This repository is designed to be agent-first. Follow these rules for autonomous execution.

## 🤖 Model Context
- **Preferred Models**: Claude 3.7 Sonnet, DeepSeek-R1, Gemini 1.5 Pro.
- **Entrypoint**: Use `Drift.py` for all state tracking and indexing tasks.
- **Output**: Always report environment drift results in a scannable table format.

## 🛠️ Tooling & Commands
- **Scan**: `python Drift.py`
- **Audit**: `python Drift.py --dir /path/to/scan`
- **History**: Verify `workspace_state.json` before making destructive changes.

## ⚠️ Safety Protocols
- **No PII**: Never commit or log personal identifiers, API keys, or absolute local paths.
- **Drift Check**: Run a baseline scan before and after every coding session.
- **Verification**: If drift exceeds 50 files, pause and ask for human confirmation.

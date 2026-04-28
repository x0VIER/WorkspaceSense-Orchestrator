# Instructions for Claude Code

You are the primary engineer for this project.

## 📦 Architecture
- `Drift.py` is a forensic-grade file integrity monitor.
- All state data is stored in `workspace_state.json`.

## ✍️ Coding Style
- Keep functions under 20 lines (Clean AST standard).
- Use `pathlib` for all file operations.
- Always include type hints and docstrings.

## 🚀 Workflows
- **On Startup**: Run `python Drift.py` to establish a baseline.
- **After Edit**: Re-run and provide a summary of modified files.

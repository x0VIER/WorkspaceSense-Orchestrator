# 🕵️‍♂️ WorkspaceSense

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/x0VIER/WorkspaceSense-Orchestrator/actions/workflows/ci.yml/badge.svg)](https://github.com/x0VIER/WorkspaceSense-Orchestrator/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Keep your workspace honest. Track every byte, detect every drift.**

WorkspaceSense is a forensic-grade tool designed to monitor your project's integrity. It captures a cryptographic "snapshot" of your files and alerts you the moment anything changes—whether it's a manual edit, a background process, or an AI agent going rogue.

---

## 🚀 Why do I need this?

If you're working with AI agents (like Codex, OpenRouter, or Hermes), you know they can be unpredictable. Sometimes they fix a bug but accidentally delete a configuration file or change a setting you didn't ask for.

WorkspaceSense acts as your **black box recorder**. Run it before and after you let an agent work on your code to see *exactly* what happened.

### 🌟 Key Features
- **Forensic Fidelity**: Uses SHA-256 hashing to ensure word-for-word accuracy.
- **Drift Detection**: Instantly spots added, modified, or deleted files.
- **Privacy First**: 100% local. No telemetry. Your code stays on your hardware.
- **Zero Noise**: Automatically ignores junk folders like `.git`, `node_modules`, and `__pycache__`.

---

## 📸 Tool in Action

<p align="center">
  <img src="demo/showcase.png" width="700" alt="WorkspaceSense Showcase">
  <br>
  <i>WorkspaceSense detecting environment drift after a session.</i>
</p>

---

## 🤖 For AI Agents (Codex, Hermes, etc.)

You can point your AI agent directly at this tool to ensure it remains accountable. Use this prompt pattern:

> "Before you start, run `python WorkspaceSense.py` to index the current state. After you finish your task, run it again and report any environment drift to confirm only the requested changes were made."

This forces the agent to acknowledge its footprint and makes debugging "invisible" errors much easier.

---

## 🛠 Setup & Usage

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/x0VIER/WorkspaceSense-Orchestrator.git
   cd WorkspaceSense-Orchestrator
   ```
2. (Optional) Install testing tools:
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start
To scan your current folder:
```bash
python WorkspaceSense.py
```

To scan a specific project elsewhere:
```bash
python WorkspaceSense.py --dir /path/to/your/project
```

### Understanding the Output
- **`workspace_state.json`**: This is your snapshot. Keep it safe; it's the source of truth.
- **`codex_redundancy.log`**: A forensic log of every scan and any errors encountered.

---

## 🛣 Roadmap (100x Improvements)
- [ ] **Real-time Watcher**: Instant desktop notifications when files change.
- [ ] **Rich CLI**: Beautiful dashboards and tables for terminal users.
- [ ] **Git Integration**: Direct integration with your branch state.
- [ ] **Cloud-lite Sync**: Encrypted, opt-in state sharing for distributed teams.

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for more information.

Built with ⚡ by **x0VIER**

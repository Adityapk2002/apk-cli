# 🤖 APK Smart CLI

> An intelligent command-line interface powered by Groq AI for shell commands, Git operations, and file management.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/AI-Groq%20Powered-purple.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

🧠 **AI Assistant** - Ask anything with `?`  
📝 **Command Explainer** - Understand shell commands  
🔧 **Smart Git Helper** - Natural language Git operations  
🔍 **File Search** - Find files with plain English  
⚡ **Auto-fix** - AI suggests fixes for failed commands  
🎨 **Beautiful UI** - Rich terminal interface with history

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install openai prompt_toolkit rich PyYAML

# Run
python3 cli.py

# Enter your Groq API key when prompted
```

---

## 📖 Usage

```bash
?what is docker                    # Ask AI anything
!explain tar -xzvf file.tar.gz    # Explain commands
!git status                        # Smart Git helper
!find python files                 # Natural language search
ls -la                             # Regular shell commands
!help                              # Show all commands
```

---

## 🎯 Key Commands

| Command | Description |
|---------|-------------|
| `?<query>` | Ask AI assistant |
| `!explain <cmd>` | Explain shell command |
| `!git <action>` | Git operations |
| `!find <query>` | File search |
| `!models` | List AI models |
| `!help` | Show help |

---

## 📁 Project Structure

```
apk-smart-cli/
├── CLI.py              # Main CLI application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── config.yaml         # API key config (auto-generated)
└── plugins/
    ├── __init__.py     # Plugin package
    ├── groq_utils.py   # AI utilities
    ├── git_helper.py   # Git commands
    └── file_search.py  # File search
```

---

## 🔧 Configuration

First run creates `config.yaml`:
```yaml
GROQ_API_KEY: your_key_here
```

Get your API key: [console.groq.com](https://console.groq.com)

---

## 💡 Examples

**AI Questions:**
```bash
APK CLI ~> ?explain recursion in python
```

**Command Help:**
```bash
APK CLI ~> !explain grep -r "text" .
╭──── Explanation ────╮
│ Recursively search  │
│ for "text" in all   │
│ files               │
╰─────────────────────╯
```

**Git Workflow:**
```bash
APK CLI ~/project> !git add .
APK CLI ~/project> !git commit "Added feature"
APK CLI ~/project> !git push
```

**Smart Error Fix:**
```bash
APK CLI ~> pythn --version
╭─── Try This ───╮
│ python --version│
╰────────────────╯
```

---

## 🐛 Troubleshooting

**Plugin errors?** Create `plugins/__init__.py`  
**API errors?** Check `config.yaml` has valid key  
**Import errors?** Run `pip install -r requirements.txt`

---

## 🤝 Contributing

Pull requests welcome! Feel free to add features, fix bugs, or improve documentation.

---

<div align="center">
⭐ Star this repo if you find it useful!
</div>

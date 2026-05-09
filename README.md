# FileCLI

**English** | [**Русский**](README_RU.md)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Termux-lightgrey?style=flat-square)]()
[![License](https://img.shields.io/badge/license-GPL--3.0-green?style=flat-square)](LICENSE)

An interactive terminal tool that merges your project files into a single document, ready to paste into any LLM context window.

## What is FileCLI?

When working with AI coding assistants (Claude, GPT, Gemini, etc.), you often need to share your codebase as context. FileCLI solves this: point it at a folder, pick the files you want, and get a clean merged `.txt` in seconds.

```
python merge_files.py
```

**Key capabilities:**

- Navigate your project with a keyboard-driven TUI, no dependencies required
- Select or deselect individual files; FileCLI remembers your choices per directory
- Drag and drop folders or files directly into the terminal (Windows, Linux, Termux)
- Skips binary files, build artifacts, and `node_modules` automatically
- Supports English, Russian, and Chinese interfaces

## Installation

FileCLI requires no third-party packages, just Python 3.8 or later.

**Clone and run:**

```bash
git clone https://github.com/Datvex/FileCLI.git
cd FileCLI
python merge_files.py
```

**Or download the script directly:**

```bash
curl -O https://raw.githubusercontent.com/Datvex/FileCLI/main/merge_files.py
python merge_files.py
```

| Platform | Supported |
| --- | --- |
| Windows 10/11 | yes |
| Linux | yes |
| Termux | yes |

## Usage

1. Launch the script.
2. Press `1` to start, then enter a folder path or drag and drop it into the terminal.
3. Toggle files on/off by typing their numbers. Press `0` to confirm.
4. Find the merged `.txt` file in your Downloads folder (or a custom path from Settings).

The output file is formatted with clear separators between files, so any LLM can parse it easily.

## Settings

Press `2` from the main menu to open Settings:

- **Output path** – change where merged files are saved
- **Language** – switch between English, Russian, and Chinese

Settings are saved automatically across sessions.

## License

[GPL-3.0](LICENSE)

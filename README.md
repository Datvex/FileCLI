<div align="center">

# 🗃️ DataExtractor TUI

**A beautiful, zero-dependency Terminal User Interface for extracting and merging file contents.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat-square)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat-square)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg?style=flat-square)](#)

<img src="https://github.com/user-attachments/assets/32d20451-e315-423a-9673-beefdc1e3944" alt="DataExtractor TUI Interface" width="850" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-top: 20px; margin-bottom: 20px;"/>

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration)

</div>

---

## 💡 Overview

**DataExtractor TUI** is a highly optimized, cross-platform command-line tool designed to seamlessly aggregate text data from multiple files and directories. Originally built to prepare massive codebases for Large Language Model (LLM) context windows, it features a stunning, hardware-accelerated terminal interface with native mouse support, smart encoding detection, and intelligent file filtering.

## ✨ Features

- **Rich Terminal UI**: Smooth rendering, floating modals, and raw input handling for a GUI-like experience in your terminal.
- **Native Mouse Support**: Full mouse integration on Windows (clicks, hover, selection) via WinAPI.
- **Zero Dependencies**: Built entirely on Python's standard library. No `pip install` required.
- **Smart Filtering**: Automatically ignores binary files and common development directories (`node_modules`, `.git`, `venv`, `__pycache__`, etc.).
- **Drag & Drop**: Seamlessly drag and drop files or folders directly into the terminal window.
- **Auto-Encoding Detection**: Intelligently detects and handles `UTF-8`, `UTF-8-SIG`, `UTF-16`, `CP1251`, and `CP1252`.
- **State Memory**: Remembers your previously disabled files, output paths, and language preferences.
- **Internationalization (i18n)**: Native support for **English**, **Russian**, and **Chinese**.

## 🚀 Installation

Since DataExtractor TUI has **zero external dependencies**, installation is as simple as downloading the script.

```bash
# Clone the repository
git clone https://github.com/yourusername/data-extractor-tui.git

# Navigate to the directory
cd data-extractor-tui

# Run the application
python main.py
```

## 🕹️ Usage

1. **Launch the Tool**: Run `python main.py`.
2. **Select Action**: Press `1` to start extraction or `2` to open Settings.
3. **Input Target**: Type the path to your directory or simply **Drag & Drop** a folder/files into the terminal.
4. **Toggle Files**: 
   - Type the number of a file to toggle its selection.
   - Type `0` to confirm and begin the extraction process.
5. **Output**: The merged data will be saved to your configured output path (defaults to your `Downloads` folder) as `extracted_data_YYYYMMDD_HHMMSS.txt`.

### Keyboard & Mouse Controls

| Action | Shortcut / Input |
| :--- | :--- |
| **Navigate Menus** | `Up` / `Down` Arrows |
| **Select Item** | `Enter` or **Left Mouse Click** |
| **Go Back / Cancel** | `Esc` or `Ctrl+C` |
| **Toggle File** | Enter file number (e.g., `1`, `4`) |
| **Start Extraction** | `0` |

## ⚙️ Configuration

The application automatically saves your preferences (language, output directory, and file exclusion memory) to a local JSON file:

- **Path**: `~/.merge_files_memory.json`

You can safely delete this file at any time to restore the application to its default factory settings.

## 🤝 Contributing

We welcome contributions! If you'd like to improve the tool, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<div align="center">
  <sub>Built with ❤️ for developers and AI engineers.</sub>
</div>

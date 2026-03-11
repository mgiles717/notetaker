# Notetaker CLI

pure vibe coded.

might wanna change the data dir if you are using this, I keep my Notes in my root, so this works for me.

A simple command-line note-taking tool with an interactive file browser.

## Features

- Interactive file browser with arrow key navigation
- Create new markdown notes
- Open notes in nvim
- Create directories to organize notes
- Delete notes
- All notes stored in `~/notes`

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the CLI tool
pip install -e .
```

## Usage

Simply run:

```bash
notetaker
```

### Navigation

- Use **arrow keys** to navigate
- Press **Enter** to select a file/directory
- When a file is selected, press **Enter** to open in nvim or **d** to delete
- Select **[+] Create New Note** to create a new markdown file
- Select **[D] Create New Directory** to create a new folder
- Select **[Q] Quit** to exit

## Notes Directory

All notes are stored in `~/notes` by default. The directory will be created automatically on first run.

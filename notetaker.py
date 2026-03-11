#!/usr/bin/env python3
"""
Simple CLI note-taking tool with interactive file browser.
"""
import os
import sys
import subprocess
from pathlib import Path
from simple_term_menu import TerminalMenu


NOTES_DIR = Path.home() / "Notes"


def ensure_notes_dir():
    """Ensure the notes directory exists."""
    NOTES_DIR.mkdir(exist_ok=True)


def get_file_tree(directory):
    """Get all markdown files and subdirectories in the given directory."""
    items = []

    # Add parent directory option if not at root
    if directory != NOTES_DIR:
        items.append(("../", directory.parent, "dir"))

    # Get all items in current directory
    try:
        for item in sorted(directory.iterdir()):
            if item.is_dir():
                items.append((f"{item.name}/", item, "dir"))
            elif item.suffix == ".md":
                items.append((item.name, item, "file"))
    except PermissionError:
        pass

    return items


def create_new_file(directory):
    """Prompt user to create a new markdown file."""
    print("\n" + "="*50)
    print("Create New Note")
    print("="*50)
    filename = input("Enter filename (without .md) or press Enter to cancel: ").strip()

    if not filename:
        print("Cancelled.")
        return None

    # Add .md extension if not present
    if not filename.endswith(".md"):
        filename += ".md"

    filepath = directory / filename

    # Create the file if it doesn't exist
    if not filepath.exists():
        filepath.touch()
        print(f"Created: {filepath}")

    return filepath


def delete_item(item_path):
    """Delete a file or directory."""
    print(f"\nAre you sure you want to delete: {item_path.name}? (y/N): ", end="")
    confirm = input().strip().lower()

    if confirm == 'y':
        if item_path.is_file():
            item_path.unlink()
            print(f"Deleted: {item_path.name}")
        elif item_path.is_dir():
            try:
                item_path.rmdir()
                print(f"Deleted: {item_path.name}")
            except OSError:
                print(f"Error: Directory not empty: {item_path.name}")
        return True
    return False


def open_in_nvim(filepath):
    """Open a file in nvim."""
    try:
        subprocess.run(["nvim", str(filepath)])
    except FileNotFoundError:
        print("Error: nvim not found. Please install neovim.")
        sys.exit(1)


def create_new_directory(directory):
    """Create a new subdirectory."""
    print("\n" + "="*50)
    print("Create New Directory")
    print("="*50)
    dirname = input("Enter directory name or press Enter to cancel: ").strip()

    if not dirname:
        print("Cancelled.")
        return None

    dirpath = directory / dirname
    dirpath.mkdir(exist_ok=True)
    print(f"Created: {dirpath}")
    return dirpath


def main():
    """Main application loop."""
    ensure_notes_dir()
    current_dir = NOTES_DIR

    while True:
        items = get_file_tree(current_dir)

        # Build menu options
        menu_items = [item[0] for item in items]
        menu_items.extend([
            "────────────────────────────",
            "[n] Create New Note",
            "[d] Create New Directory",
            "[q] Quit"
        ])

        # Show current directory
        rel_path = current_dir.relative_to(NOTES_DIR) if current_dir != NOTES_DIR else Path(".")
        title = f"\n  Notes Browser: ~/{rel_path}\n"

        # Create and show menu
        menu = TerminalMenu(
            menu_items,
            title=title,
            menu_cursor="→ ",
            menu_cursor_style=("fg_cyan", "bold"),
            menu_highlight_style=("bg_cyan", "fg_black"),
            cycle_cursor=True,
            clear_screen=True,
        )

        selection_index = menu.show()

        if selection_index is None or selection_index == len(menu_items) - 1:
            # Quit
            print("\nGoodbye!")
            break

        # Handle selection
        if selection_index < len(items):
            # Selected an existing item
            _, item_path, item_type = items[selection_index]

            if item_type == "dir":
                current_dir = item_path
            elif item_type == "file":
                # Check if user wants to delete (shift+d or just open)
                print(f"\nSelected: {item_path.name}")
                print("Press Enter to open, 'd' to delete, or 'q' to cancel: ", end="")
                action = input().strip().lower()

                if action == 'd':
                    delete_item(item_path)
                    input("\nPress Enter to continue...")
                elif action != 'q':
                    open_in_nvim(item_path)

        elif selection_index == len(items):
            # Separator - do nothing, just continue
            continue

        elif selection_index == len(items) + 1:
            # Create new note
            new_file = create_new_file(current_dir)
            if new_file:
                input("\nPress Enter to open in nvim...")
                open_in_nvim(new_file)

        elif selection_index == len(items) + 2:
            # Create new directory
            create_new_directory(current_dir)
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

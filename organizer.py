#!/usr/bin/env python3
"""
File Organizer CLI

Automatically organizes files in a directory into categorized folders
based on their file extensions.

Usage:
    python organizer.py /path/to/messy/folder
    python organizer.py /path/to/folder --dry-run
    python organizer.py /path/to/folder --undo
"""

import os
import sys
import json
import shutil
import argparse
import logging
from datetime import datetime
from pathlib import Path

# File extension categories
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs", ".ts", ".jsx", ".json", ".xml", ".yaml", ".yml"],
    "Executables": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}

LOG_FILE = ".organizer_log.json"


def setup_logging(verbose=False):
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
    )


def get_category(extension):
    """Return the category for a given file extension."""
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize(target_dir, dry_run=False, verbose=False):
    """
    Organize files in the target directory into category folders.

    Args:
        target_dir: Path to the directory to organize.
        dry_run: If True, only show what would happen without moving files.
        verbose: If True, show detailed output.

    Returns:
        Dictionary mapping moved files to their destinations.
    """
    target = Path(target_dir).resolve()

    if not target.is_dir():
        logging.error(f"Error: '{target}' is not a valid directory.")
        sys.exit(1)

    moves = {}
    stats = {}

    # Get all files in the directory (not subdirectories)
    files = [f for f in target.iterdir() if f.is_file() and f.name != LOG_FILE]

    if not files:
        logging.info("No files to organize.")
        return moves

    logging.info(f"{'[DRY RUN] ' if dry_run else ''}Organizing {len(files)} files in: {target}\n")

    for file_path in sorted(files):
        ext = file_path.suffix
        if not ext:
            category = "Other"
        else:
            category = get_category(ext)

        dest_dir = target / category
        dest_path = dest_dir / file_path.name

        # Handle duplicate filenames
        if dest_path.exists():
            stem = file_path.stem
            counter = 1
            while dest_path.exists():
                dest_path = dest_dir / f"{stem}_{counter}{ext}"
                counter += 1

        # Track stats
        stats[category] = stats.get(category, 0) + 1

        if dry_run:
            logging.info(f"  Would move: {file_path.name} -> {category}/")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(file_path), str(dest_path))
            logging.info(f"  Moved: {file_path.name} -> {category}/")

        moves[str(file_path)] = str(dest_path)

    # Print summary
    logging.info(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    for category, count in sorted(stats.items()):
        logging.info(f"  {category}: {count} file(s)")
    logging.info(f"  Total: {sum(stats.values())} file(s)")

    # Save log for undo (only if not dry run)
    if not dry_run and moves:
        log_path = target / LOG_FILE
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "moves": moves,
        }
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)
        logging.info(f"\nLog saved to {LOG_FILE} (use --undo to reverse)")

    return moves


def undo(target_dir):
    """
    Reverse the last organize operation using the log file.

    Args:
        target_dir: Path to the organized directory.
    """
    target = Path(target_dir).resolve()
    log_path = target / LOG_FILE

    if not log_path.exists():
        logging.error("No organizer log found. Nothing to undo.")
        sys.exit(1)

    with open(log_path) as f:
        log_data = json.load(f)

    moves = log_data["moves"]
    logging.info(f"Undoing {len(moves)} move(s) from {log_data['timestamp']}...\n")

    restored = 0
    for original, current in moves.items():
        current_path = Path(current)
        original_path = Path(original)

        if current_path.exists():
            shutil.move(str(current_path), str(original_path))
            logging.info(f"  Restored: {original_path.name}")
            restored += 1

            # Remove empty category folder
            parent = current_path.parent
            if parent.is_dir() and not list(parent.iterdir()):
                parent.rmdir()
                logging.debug(f"  Removed empty folder: {parent.name}/")
        else:
            logging.warning(f"  Skipped (not found): {current_path}")

    # Remove log file
    log_path.unlink()
    logging.info(f"\nRestored {restored} file(s). Log file removed.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Organize files in a directory into categorized folders by extension.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py ~/Downloads
  python organizer.py ~/Desktop --dry-run
  python organizer.py ~/Downloads --undo
  python organizer.py . --verbose
        """,
    )
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--undo", action="store_true", help="Reverse the last organize operation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.undo:
        undo(args.directory)
    else:
        organize(args.directory, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()

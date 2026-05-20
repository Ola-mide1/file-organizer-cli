# File Organizer CLI

A Python command-line tool that automatically organizes files in a directory into categorized folders based on their file extensions.

## Features

- Sorts files into categories: Images, Documents, Videos, Audio, Archives, Code, and more
- **Dry run mode** to preview changes before moving anything
- **Undo support** to reverse the last organization
- Handles duplicate filenames automatically
- Detailed logging and summary output
- No external dependencies (uses Python standard library only)

## Installation

```bash
git clone https://github.com/Ola-mide1/file-organizer-cli.git
cd file-organizer-cli
```

No dependencies to install — uses only the Python standard library.

## Usage

```bash
# Organize files in a directory
python organizer.py ~/Downloads

# Preview what would happen (no files moved)
python organizer.py ~/Desktop --dry-run

# Undo the last organization
python organizer.py ~/Downloads --undo

# Verbose output
python organizer.py . --verbose
```

## File Categories

| Category | Extensions |
|----------|-----------|
| Images | .jpg, .png, .gif, .svg, .webp, ... |
| Documents | .pdf, .docx, .txt, .xlsx, .pptx, .csv, ... |
| Videos | .mp4, .avi, .mkv, .mov, ... |
| Audio | .mp3, .wav, .flac, .aac, ... |
| Archives | .zip, .rar, .7z, .tar.gz, ... |
| Code | .py, .js, .html, .css, .json, ... |
| Other | Everything else |

## Example Output

```
Organizing 15 files in: /home/user/Downloads

  Moved: photo.jpg -> Images/
  Moved: report.pdf -> Documents/
  Moved: song.mp3 -> Audio/
  Moved: script.py -> Code/
  Moved: backup.zip -> Archives/

Summary:
  Archives: 1 file(s)
  Audio: 1 file(s)
  Code: 1 file(s)
  Documents: 1 file(s)
  Images: 1 file(s)
  Total: 5 file(s)

Log saved to .organizer_log.json (use --undo to reverse)
```

## License

MIT

# TXT to HTML Batch Converter

This script converts all `.txt` files in a selected folder to stylish `.html` files with modern themes and link extraction.

## Features
- Batch convert all `.txt` files in a folder to `.html`.
- Extracts topics, video links, and PDF links from each file.
- 10+ ultra-modern, colorful toggle themes (with emojis).
- Custom converter name (𓆰ＳＨＩＶ𓆪), date/time, and batch name from file name.
- Choose input and output folders via command-line or interactive prompt.

## Usage

### 1. Basic Usage (Default Folders)
```bash
python3 txt_to_html_converter.py
```
- Input folder: `txt/`
- Output folder: `HTML/`

### 2. Manual Folder Selection (Interactive)
Just run:
```bash
python3 txt_to_html_converter.py
```
You will be prompted to enter the input and output folder paths. Press Enter to use defaults.

### 3. Command-Line Arguments
```bash
python3 txt_to_html_converter.py -i <input_folder> -o <output_folder>
```
- Replace `<input_folder>` with your folder containing `.txt` files.
- Replace `<output_folder>` with your desired output folder for `.html` files.

## Example
```bash
python3 txt_to_html_converter.py -i txt -o HTML
```

## Output
- Each `.txt` file will be converted to a `.html` file in the output folder.
- Open the generated `.html` files in your browser to view the results and toggle themes.

## Requirements
- Python 3.x
- No external dependencies required.

## Notes
- The script will create the output folder if it does not exist.
- The HTML files are styled and interactive, with theme toggling and emoji support.

---

**Made with ❤️ by 𓆰ＳＨＩＶ𓆪**

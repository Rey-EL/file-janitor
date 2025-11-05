# FileJanitor

## Description

This is a Python utility script designed to clean and organize a folder by identifying and removing duplicate files and empty folders. It's built to be safe, interactive, and efficient.

## Core Features

*   **Finds Duplicates:** Scans a target directory and all its subdirectories to find duplicate files.
*   **SHA-256 Hashing:** Uses secure SHA-256 hashing to accurately identify duplicates based on their content, not just their names.
*   **Smart Deletion:** When duplicates are found, the script keeps the newest version of the file (based on modification time) and prompts to delete the older copies.
*   **Safe by Default:** Includes a "Backup" folder protection rule, preventing the script from deleting any file that has "backup" in its path.
*   **Finds Empty Folders:** Recursively searches for and identifies folders that are completely empty (or only contain empty subfolders).

## User-Friendly

*   Uses `tkinter` to provide a graphical folder selection dialog at the start.
*   Uses `tqdm` to show a live progress bar during the file-scanning phase.
*   Prompts the user with a single "y/n" confirmation before deleting all found duplicates and all empty folders.

## Logging

*   Generates a complete `FileJanitor_log_...txt` report detailing all actions taken, files deleted, and errors encountered.

## How to Use

1.  Run the script from your terminal: `python3 FileJanitor.py`
2.  A dialog box will appear. Select the folder you wish to scan.
3.  The script will scan for duplicates and empty folders.
4.  Review the findings and answer the (y/n) prompts to approve deletions.
5.  A final log file will be saved in the same directory where the script was run.
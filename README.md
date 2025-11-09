# file-janitor

FileJanitor is a Python utility script designed to clean and organize folders by identifying and removing duplicate files and empty directories. It uses a graphical interface for folder selection and provides clear terminal output, making it a safe and user-friendly tool for disk cleanup.

---

## Key Features

*   **Finds Duplicate Files:** Scans a target directory and all its subdirectories to find files with identical content, regardless of their name.
*   **Accurate Hashing:** Uses the secure SHA-256 hashing algorithm to accurately identify true duplicates based on content.
*   **Smart Deletion Logic:** When duplicates are found, the script automatically identifies the newest version of the file (by modification date) to keep and flags the older copies for deletion.
*   **Finds Empty Folders:** Recursively searches for and identifies folders that are completely empty.
*   **Safety First:**
    *   Prompts the user for a single confirmation before deleting all flagged files and another before deleting empty folders. No action is taken without approval.
    *   Includes a "backup" folder protection rule, preventing the script from deleting any file located in a path containing the word "backup".
*   **User-Friendly Interface:**
    *   Uses `tkinter` for a simple graphical dialog to select the target folder.
    *   Displays a `tqdm` progress bar during the file scanning process.
*   **Detailed Logging:** Generates a comprehensive `FileJanitor_log_...txt` report in the script's directory, detailing all actions taken, files deleted, and any errors encountered.

---

## Security Considerations

FileJanitor is a local utility script and does not interact with networks or external services, which means it is not directly susceptible to many common web-based vulnerabilities like those in the OWASP Top 10. However, users should always:

*   **Backup Important Data:** Before running any file management utility, ensure critical data is backed up.
*   **Understand File Operations:** Be aware of the files being processed and confirmed for deletion.
*   **Keep System Updated:** Ensure your operating system and Python environment are kept up-to-date with the latest security patches.

---

## License

This project is licensed under the [MIT License](./LICENSE.md) - see the LICENSE.md file for details.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements, bug reports, or want to add new features, please feel free to open an issue or submit a pull request.

---

## Installation & Setup

To use FileJanitor, you need Python 3.

1.  **Navigate to the project directory:**
    ```bash
    cd file-janitor
    ```

2.  **Install dependencies:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    # Create and activate a virtual environment (optional but recommended)
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install the required packages from the requirements.txt file
    pip install -r requirements.txt
    ```

---

## Usage

1.  **Run the script from your terminal:**
    ```bash
    python3 file_janitor.py
    ```

2.  **Select a Folder:** A graphical dialog box will appear. Navigate to and select the folder you wish to scan.

3.  **Review and Confirm:** The script will scan the directory and then present its findings. It will prompt you to approve the deletion of old duplicate files and empty folders separately.
    ```
    Do you want to delete all 15 of these files? (y/n): y
    ```

4.  **Check the Log:** After the script finishes, a log file named `FileJanitor_log_...txt` will be created in the same directory. You can review it for a detailed record of all operations.

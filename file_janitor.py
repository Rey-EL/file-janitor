import os
import hashlib
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set
from tqdm import tqdm

# --- Part 1: Core Scanning Functions ---

def hash_file(path: str, blocksize: int = 65536) -> str:
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            buf = f.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(blocksize)
        return hasher.hexdigest()
    except (IOError, PermissionError):
        return None

def find_duplicates(folder: str) -> Dict[str, List[str]]:
    """Finds duplicate files in a folder with a progress bar."""
    print("\n🔎 Searching for duplicate files...")
    all_files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        # NEW RULE: Prevent the script from scanning its own project folder
        if 'filejanitor' in os.path.normcase(dirpath):
            continue
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                if os.path.getsize(file_path) > 0:
                    all_files.append(file_path)
            except OSError:
                continue

    hashes = defaultdict(list)
    for file_path in tqdm(all_files, desc="Scanning files", unit="file"):
        file_hash = hash_file(file_path)
        if file_hash:
            hashes[file_hash].append(file_path)
            
    print(f"✅ Finished scanning {len(all_files)} files.")
    return {hash_val: paths for hash_val, paths in hashes.items() if len(paths) > 1}

def find_empty_folders(folder: str) -> List[str]:
    """Finds folders that contain no files, even in their subdirectories."""
    print("\n📁 Searching for empty folders...")
    empty_folders = []
    non_empty_dirs: Set[str] = set()
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        is_non_empty = bool(filenames)
        for dirname in dirnames:
            if os.path.join(dirpath, dirname) in non_empty_dirs:
                is_non_empty = True
                break
        if is_non_empty:
            non_empty_dirs.add(dirpath)
        else:
            empty_folders.append(dirpath)
    print("✅ Finished searching for empty folders.")
    return empty_folders

# --- Part 2: Deletion and Reporting Logic ---

def handle_duplicates(duplicates: Dict[str, List[str]], report_lines: List[str]):
    """
    Finds all eligible duplicate files, presents them in a single list,
    and asks for a single confirmation to delete them all.
    """
    if not duplicates:
        report_lines.append("\n🎉 No duplicate files found!")
        return

    print("\n--- Preparing Duplicate Deletion Plan ---")
    
    all_files_to_delete = []
    
    for paths in duplicates.values():
        if not paths:
            continue

        try:
            file_to_keep = max(paths, key=os.path.getmtime)
            older_files = [p for p in paths if p != file_to_keep]
            
            for path in older_files:
                if 'backup' not in os.path.normcase(path):
                    all_files_to_delete.append(path)
                else:
                    report_lines.append(f"  PROTECTED (in backup folder): {path}")

        except FileNotFoundError:
            continue
    
    if not all_files_to_delete:
        print("✅ No deletable duplicate files found (all duplicates are either the newest version or in a backup folder).")
        report_lines.append("\nNo deletable duplicate files found.")
        return
        
    print(f"\nFound {len(all_files_to_delete)} older duplicate file(s) that can be deleted:")
    for path in all_files_to_delete:
        print(f"  -> {path}")
        
    user_input = input(f"\nDo you want to delete all {len(all_files_to_delete)} of these files? (y/n): ").lower()
    
    if user_input != 'y':
        print("Skipping deletion.")
        report_lines.append("\nUser skipped duplicate file deletion.")
        return

    deleted_count = 0
    print("Deleting files...")
    for path in all_files_to_delete:
        try:
            os.remove(path)
            action_msg = f"  DELETED: {path}"
            print(action_msg)
            report_lines.append(action_msg)
            deleted_count += 1
        except OSError as e:
            error_msg = f"  ERROR: Could not delete {path}. Reason: {e}"
            print(error_msg)
            report_lines.append(error_msg)
            
    report_lines.append(f"\nSummary: Deleted {deleted_count} duplicate file(s).")


def handle_empty_folders(empty_folders: List[str], report_lines: List[str]):
    """Interactively handles deletion of empty folders."""
    if not empty_folders:
        report_lines.append("\n🎉 No empty folders found!")
        return
        
    print("\n--- Empty Folder Actions ---")
    print("The following empty folders were found:")
    empty_folders.sort()
    for path in empty_folders:
        print(f"  -> {path}")

    user_input = input("\nDo you want to delete ALL of these empty folders? (y/n): ").lower()
    if user_input != 'y':
        report_lines.append("\nSkipped empty folder deletion.")
        return

    deleted_count = 0
    for path in sorted(empty_folders, key=len, reverse=True):
        try:
            os.rmdir(path)
            action_msg = f"  DELETED: {path}"
            print(action_msg)
            report_lines.append(action_msg)
            deleted_count += 1
        except OSError as e:
            error_msg = f"  ERROR: Could not delete {path}. Reason: {e}"
            print(error_msg)
            report_lines.append(error_msg)
    report_lines.append(f"\nSummary: Deleted {deleted_count} empty folder(s).")

# --- Part 3: Main Program Logic ---

def main():
    """Main function to run the scanner and display results."""
    root = tk.Tk()
    root.withdraw()

    print("Please select the folder for FileJanitor to scan.")
    target_folder = filedialog.askdirectory(title="Select a Folder to Scan")

    if not target_folder:
        print("No folder selected. Exiting.")
        return

    scan_time = datetime.now()
    report_lines = [
        "==========================",
        "   FileJanitor Report   ",
        "==========================",
        f"\nScan conducted on: {scan_time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Target Folder: {target_folder}\n"
    ]

    print(f"--- Starting Scan on: {target_folder} ---")

    duplicates = find_duplicates(target_folder)
    empty_folders = find_empty_folders(target_folder)
    
    report_lines.append(f"Found {len(duplicates)} set(s) of duplicate files.")
    report_lines.append(f"Found {len(empty_folders)} empty folder(s).")
    
    handle_duplicates(duplicates, report_lines)
    handle_empty_folders(empty_folders, report_lines)

    log_filename = f"FileJanitor_log_{scan_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    final_report = "\n".join(report_lines)

    try:
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write(final_report)
        print(f"\n--- Scan Complete ---")
        print(f"✅ Full report saved to: {log_filename}")
    except IOError as e:
        print(f"\n--- Scan Complete ---")
        print(f"⚠️ Error: Could not save log file. Reason: {e}")
    
    print("\nFinal Report Summary:")
    print(final_report)


if __name__ == "__main__":
    main()

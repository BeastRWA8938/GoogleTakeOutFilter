import os
import shutil
import hashlib
from pathlib import Path

# Define the main output directory and subdirectories
SORTED_DIR = 'Sorted Files'
PHOTOS_DIR = os.path.join(SORTED_DIR, 'Photos')
VIDEOS_DIR = os.path.join(SORTED_DIR, 'Videos')
DUPLICATES_DIR = os.path.join(SORTED_DIR, 'Duplicates')

# Supported file extensions
PHOTO_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.3gp', '.webm')

def get_file_hash(filepath):
    """Calculate and return the hash of the file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError) as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def ensure_directory_exists(directory):
    """Ensure the directory exists."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def get_unique_filename(dest_path):
    """Generate a unique filename if the destination already exists."""
    if not os.path.exists(dest_path):
        return dest_path
    
    base, ext = os.path.splitext(dest_path)
    counter = 1
    
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def copy_file(file_path, dest_dir, file_hash_cache):
    """Copy file to the destination directory, handling duplicates by hash comparison."""
    ensure_directory_exists(dest_dir)
    
    # Get file hash for duplicate detection
    file_hash = get_file_hash(file_path)
    if file_hash is None:
        print(f"Skipping file due to read error: {file_path}")
        return False
    
    # Check if we've seen this hash before
    if file_hash in file_hash_cache:
        # This is a duplicate - copy to duplicates folder
        filename = os.path.basename(file_path)
        duplicate_dest = os.path.join(DUPLICATES_DIR, filename)
        duplicate_dest = get_unique_filename(duplicate_dest)
        
        try:
            shutil.copy2(file_path, duplicate_dest)
            print(f"Duplicate found: {filename} -> Duplicates/{os.path.basename(duplicate_dest)}")
            return False
        except (IOError, OSError) as e:
            print(f"Error copying duplicate {file_path}: {e}")
            return False
    else:
        # First time seeing this hash - copy to appropriate folder
        filename = os.path.basename(file_path)
        dest_path = os.path.join(dest_dir, filename)
        dest_path = get_unique_filename(dest_path)
        
        try:
            shutil.copy2(file_path, dest_path)
            file_hash_cache[file_hash] = dest_path
            return True
        except (IOError, OSError) as e:
            print(f"Error copying file {file_path}: {e}")
            return False

def scan_and_organize_files():
    """Scan the current directory and organize photos and videos."""
    script_dir = os.getcwd()
    
    # Create the main sorted directory structure
    ensure_directory_exists(PHOTOS_DIR)
    ensure_directory_exists(VIDEOS_DIR)
    ensure_directory_exists(DUPLICATES_DIR)
    
    print(f"Organizing files from: {script_dir}")
    print(f"Output directory: {os.path.join(script_dir, SORTED_DIR)}")
    print("=" * 50)
    
    # Count total files for progress tracking
    print("Scanning directories...")
    total_files = 0
    directories_to_scan = []
    
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        # Skip the script file, sorted directory, and any hidden files/folders
        if (os.path.isdir(item_path) and 
            item != SORTED_DIR and 
            not item.startswith('.') and 
            not item.startswith('__')):
            directories_to_scan.append(item_path)
    
    if not directories_to_scan:
        print("No directories found to scan.")
        return
    
    print(f"Found {len(directories_to_scan)} directories to scan:")
    for dir_path in directories_to_scan:
        print(f"  - {os.path.basename(dir_path)}")
    
    # Count files in all directories
    for dir_path in directories_to_scan:
        for root, dirs, files in os.walk(dir_path):
            total_files += len(files)
    
    if total_files == 0:
        print("No files found to process.")
        return
    
    print(f"\nFound {total_files} total files to process.")
    
    # Process files
    processed_files = 0
    copied_photos = 0
    copied_videos = 0
    duplicates_found = 0
    file_hash_cache = {}  # Track file hashes to detect duplicates
    
    for dir_path in directories_to_scan:
        print(f"\nProcessing directory: {os.path.basename(dir_path)}")
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_lower = file.lower()
                
                if file_lower.endswith(PHOTO_EXTENSIONS):
                    if copy_file(file_path, PHOTOS_DIR, file_hash_cache):
                        copied_photos += 1
                    else:
                        duplicates_found += 1
                elif file_lower.endswith(VIDEO_EXTENSIONS):
                    if copy_file(file_path, VIDEOS_DIR, file_hash_cache):
                        copied_videos += 1
                    else:
                        duplicates_found += 1
                
                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {processed_files}/{total_files} files ({progress:.1f}%)", end='\r')
    
    print(f"\n\nOrganization completed!")
    print("=" * 50)
    print(f"Photos copied: {copied_photos}")
    print(f"Videos copied: {copied_videos}")
    print(f"Duplicates found: {duplicates_found}")
    print(f"Total files processed: {processed_files}")
    print(f"\nFiles organized in: {os.path.join(script_dir, SORTED_DIR)}")

def main():
    """Main function."""
    print("File Organizer - Photos and Videos")
    print("=" * 50)
    print("This script will organize files from all folders in the current directory.")
    print(f"Files will be copied (not moved) to a '{SORTED_DIR}' folder with subfolders:")
    print(f"  - Photos/")
    print(f"  - Videos/")
    print(f"  - Duplicates/")
    print("\nOriginal files will remain in their current locations.")
    
    # Confirm before proceeding
    confirm = input("\nProceed with file organization? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    scan_and_organize_files()

if __name__ == '__main__':
    main()

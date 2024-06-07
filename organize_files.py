import os
import shutil
import hashlib

# Define paths for storing photos and videos
PHOTOS_DIR = 'Photos'
VIDEOS_DIR = 'Videos'
DUPLICATES_DIR = 'Duplicates'

# Supported file extensions
PHOTO_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')

def get_file_hash(filepath):
    """Calculate and return the hash of the file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def ensure_directory_exists(directory):
    """Ensure the directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def move_file(file_path, dest_dir):
    """Move file to the destination directory, handling duplicates."""
    ensure_directory_exists(dest_dir)
    file_hash = get_file_hash(file_path)
    dest_path = os.path.join(dest_dir, os.path.basename(file_path))
    
    if not os.path.exists(dest_path):
        shutil.move(file_path, dest_path)
    else:
        duplicate_dir = os.path.join(dest_dir, DUPLICATES_DIR)
        ensure_directory_exists(duplicate_dir)
        move_file_with_duplicate_handling(file_path, duplicate_dir, file_hash)

def move_file_with_duplicate_handling(file_path, duplicate_dir, file_hash, suffix=''):
    """Move file to the duplicate directory with handling for nested duplicates."""
    duplicate_folder = os.path.join(duplicate_dir, f'{DUPLICATES_DIR}{suffix}')
    ensure_directory_exists(duplicate_folder)
    dest_path = os.path.join(duplicate_folder, os.path.basename(file_path))
    
    if not os.path.exists(dest_path):
        shutil.move(file_path, dest_path)
    else:
        new_suffix = str(int(suffix) + 1) if suffix.isdigit() else '1'
        move_file_with_duplicate_handling(file_path, duplicate_dir, file_hash, new_suffix)

def scan_and_move_files(root_dir):
    """Scan all files and folders and move photos and videos to appropriate directories."""
    total_files = sum([len(files) for r, d, files in os.walk(root_dir)])
    processed_files = 0
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(PHOTO_EXTENSIONS):
                move_file(file_path, PHOTOS_DIR)
            elif file.lower().endswith(VIDEO_EXTENSIONS):
                move_file(file_path, VIDEOS_DIR)
            
            processed_files += 1
            print(f"Processed {processed_files}/{total_files} files ({(processed_files/total_files)*100:.2f}%)", end='\r')
    
    print("\nScanning and moving completed.")

if __name__ == '__main__':
    # All your unzipped takeout files should be inside this folder
    root_directory = r"<Replace Path Here>"
    scan_and_move_files(root_directory)
    print("Scanning and moving completed.")

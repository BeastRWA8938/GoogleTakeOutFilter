# GoogleTakeOut Photos Organizer

This script helps you organize your Google Photos into sorted "Photos" and "Videos" folders. It is designed for people who find it difficult to shift their Google Photos to another platform or simply want a sorted collection.

## How It Works

1. The script scans all files and folders starting from a specified root directory.
2. It identifies photo and video files based on their extensions.
3. Photo files are moved to a "Photos" folder and video files to a "Videos" folder.
4. If a duplicate file is found, it is moved to a "Duplicates" folder. Nested duplicates are handled by creating subfolders like "Duplicates1", "Duplicates2", etc.

## Recommended Preprocessing

It is recommended to run [ExifTool](https://exiftool.org/) first to fix the metadata of your files. This ensures that all photos and videos have the correct metadata before running this script.

# Here is how you can use the ExifTool
https://legault.me/post/correctly-migrate-away-from-google-photos-to-icloud

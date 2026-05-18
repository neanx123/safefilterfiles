# Safe Filter Files (SFF)

v1.0.0 (in development)

By Nean

#### Video Demo: <URL HERE>

#### Description:

Safe Filter Files (SFF) is an open-source Python utility created to help users organize possible duplicate files safely and transparently!

*SFF groups files only by their size in bytes and moves them into generated folders*. This allows users to manually inspect the files and decide what should be kept or removed. Instead of deleting files or trying to confirm exact duplicates, SFF only groups and moves same-sized files. 

The project was designed with simplicity, safety, and user final decision/control as its main priorities.

## Project Idea

Many duplicate file tools automatically compare file hashes or even delete files without giving users enough control over the process. SFF was created as a safer alternative that only groups possible duplicates for manual inspection.

This can be useful for people who:
- accidentally download the same files multiple times;
- rename duplicated files;
- manage large collections of files;
- want a non-destructive organization tool.

SFF never deletes files. It only moves them into grouped folders to make inspection easier.

## How It Works

The program scans the directory where the Python script is located and analyzes only files in the main folder level, ignoring subdirectories.

- When two or more files share the same size, SFF creates a folder using this format:

_SFF_<reference_file_name>_<date>_<time>

Example:

_SFF_photo_2026-05-18_14-30-21


All files with the same size are then moved into that folder.

Since files with identical sizes may still contain different content, SFF treats them only as possible duplicates instead of confirmed duplicates.

## User Interaction

Before starting the scan, the program displays a simple terminal menu with two options:

MENU:

- Proceed
- Exit

This prevents accidental execution and improves usability.

- The interface was built using the Python Rich library to provide a cleaner and more readable terminal experience.

## Future Improvements

Possible future features include:
- optional hash comparison mode (slow and deep file content comparison);
- subdirectory scanning;
- preview mode;
- logs;
- GUI version;
- undo operation support.

## Version

v1.0.0 (in development)

## Author

By Nean
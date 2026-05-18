import sys
import subprocess
import os
import shutil
from collections import defaultdict
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
import time
from datetime import datetime


found = 0


def main():

    # =========================================================
    # "FILES" FOLDER CHECK
    # =========================================================
    MAIN_FOLDER = main_folder()

    # =========================================================
    # MENU
    # =========================================================
    menu()

    # =========================================================
    # BUILD SIZE-BASED GROUPS
    # =========================================================
    size_groups = build_size_groups(MAIN_FOLDER)

    # =========================================================
    # PROCESS GROUPS
    # =========================================================
    process_groups(size_groups, MAIN_FOLDER)

    # =========================================================
    # PROCESS COMPLETION
    # =========================================================
    if found == 0:
        print("\n0 duplicates found.")

    print("\nProcess completed.")



# =========================================================
# FILES FOLDER TO CHECK
# =========================================================
def main_folder():
    # =========================================================
    # RETURNS THE DIRECTORY WHERE THIS SCRIPT IS LOCATED
    # =========================================================
    # __file__ → path of the current Python script (may be relative)
    #
    # os.path.abspath(__file__)
    #   → converts the script path to an absolute path
    #     (removes ambiguity like ".", "..", or relative paths)
    #
    # os.path.dirname(...)
    #   → removes the file name and keeps only the folder path
    #
    # RESULT:
    #   Always returns the folder where this script is stored,
    #   regardless of where the program is executed from.
    #
    # WHY THIS MATTERS:
    #   Ensures consistent behavior across Windows, Linux, and macOS,
    #   and avoids issues caused by running the script from different
    #   working directories (os.getcwd()).
    # =========================================================

    return os.path.dirname(os.path.abspath(__file__))


# =========================================================
# MENU
# =========================================================
def menu():

    console = Console()

    while True:

        # =========================================================
        # CLEAR SCREEN (WINDOWS OR UNIX SYSTEMS)
        # =========================================================
        # Uses "cls" for Windows and "clear" for Linux/macOS
        # =========================================================
        subprocess.run(
            "cls" if os.name == "nt" else "clear",
            shell=True
        )

        title = Text("""
        Safe Filter Files v1.0.0
        """, style="bold green")
        
        description = (
            "SFF scans the current folder and groups files "
            "with identical sizes into separate folders\n\n"
            "- Groups files by size\n"
            "- Does NOT delete anything\n"
            "- Only moves files for further manual inspection")
    
        console.print(title, justify="center")
        console.print(Panel(description, border_style="green"), justify="center")
        console.print(
            Panel.fit(
                "[bold green]1[/] - Proceed\n[bold red]2[/] - Exit",
                title="[green]MAIN MENU[/green]",
                border_style="green")
        )
        choice = console.input("[bold green]Select option > [/bold green]")

        # =========================================================
        # OPTION 1: PROCEED WITH DUPLICATE SEARCH
        # =========================================================
        if choice == "1":
            console.print("[green]Searching for duplicates...[/green]")
            # Small delay to improve UX before starting process
            time.sleep(1)
            return
        # =========================================================
        # OPTION 2: EXIT PROGRAM
        # =========================================================
        elif choice == "2":
            console.print("\n[bold red]Closing...[/bold red]")
            # Small delay before closing for smoother UX
            time.sleep(1)

            # Clear screen before exiting
            subprocess.run(
                "cls" if os.name == "nt" else "clear",
                shell=True
            )
            sys.exit()
        # =========================================================
        # INVALID OPTION HANDLING
        # =========================================================
        # If user enters anything other than 1 or 2,
        # show error message and restart loop
        # =========================================================
        else:
            console.print("\n[bold red]Invalid option...[/bold red]")
            # Small delay before refreshing menu
            time.sleep(1)
            continue


# =========================================================
# GROUP FILES BY SIZE
# =========================================================
def build_size_groups(directory):

    # =====================================================
    # SIZE-BASED GROUPING DICTIONARY
    # =====================================================
    size_groupping = defaultdict(list)

    # =====================================================
    # DIRECTORY SCANNING
    # =====================================================
    for root, dirs, files in os.walk(directory):

        # =================================================
        # SORT FILES ALPHABETICALLY
        # =================================================
        files.sort(key=str.lower)

        for file in files:

            # =============================================
            # BUILD FULL FILE PATH
            # =============================================
            full_path = os.path.join(root, file)

            # =============================================
            # IGNORE SUBDIRECTORIES
            # =============================================
            if root != directory:
                continue

            try:

                # =========================================
                # GET FILE SIZE (IN BYTES)
                # =========================================
                size = os.path.getsize(full_path)

                # =========================================
                # GROUP FILES BY SIZE
                # =========================================
                size_groupping[size].append(full_path)

            except Exception as e:

                # =========================================
                # INDIVIDUAL ERROR HANDLING
                # =========================================
                print(f"Error reading {full_path}: {e}")

    # =====================================================
    # RETURN GROUPED FILES
    # =====================================================
    return size_groupping


# =========================================================
# GENERATE DESTINATION FOLDER NAME
# =========================================================
def get_folder_name(file_path):

    return os.path.splitext(os.path.basename(file_path))[0]


# =========================================================
# CREATE UNIQUE DESTINATION PATH
# =========================================================
def create_unique_path(destination_folder, filename):

    # =====================================================
    # INITIAL DESTINATION PATH
    # =====================================================
    destination_path = os.path.join(destination_folder, filename)

    # =====================================================
    # PREPARE FILE NAME COMPONENTS
    # =====================================================
    counter = 1
    base, ext = os.path.splitext(filename)

    # =====================================================
    # HANDLE FILE NAME COLLISIONS
    # =====================================================
    while os.path.exists(destination_path):

        destination_path = os.path.join(
            destination_folder,
            f"{base}_{counter}{ext}"
                                    )

        counter += 1

    # =====================================================
    # RETURN SAFE DESTINATION PATH
    # =====================================================
    return destination_path


# =========================================================
# PROCESS DUPLICATE-SIZE FILE GROUPS
# =========================================================
def process_groups(size_map, base_directory):

    # =====================================================
    # ITERATE THROUGH SIZE GROUPS
    # =====================================================
    for size, paths in size_map.items():

        # =================================================
        # SKIP NON-DUPLICATE GROUPS
        # =================================================
        if len(paths) < 2:
            continue

        # =================================================
        # SORT FILE PATHS FOR DETERMINISTIC OUTPUT
        # =================================================
        paths.sort(key=lambda p: os.path.basename(p).lower())

        # =================================================
        # REFERENCE FILE OF THE GROUP
        # =================================================
        first_file = paths[0]

        # =================================================
        # GENERATE DESTINATION FOLDER NAME
        # =================================================
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"_SFF_{get_folder_name(first_file)}_{timestamp}"

        # =================================================
        # DESTINATION FOLDER PATH
        # =================================================
        destination_folder = os.path.join(base_directory, folder_name)

        # =================================================
        # CREATE DESTINATION DIRECTORY IF NOT EXISTS
        # =================================================
        os.makedirs(destination_folder, exist_ok=True)

        # =================================================
        # GROUP PROCESSING LOG OUTPUT
        # =================================================
        print(f"\nDuplicates found ({size} bytes): - {os.path.splitext(paths[0])[0]}\\\n")

        # =================================================
        # MOVE FILES IN GROUP
        # =================================================
        for path in paths:

            # =============================================
            # EXTRACT FILE NAME ONLY
            # =============================================
            filename = os.path.basename(path)

            # =============================================
            # CREATE SAFE DESTINATION PATH
            # =============================================
            destination_path = create_unique_path(
                destination_folder,
                filename
                                                )

            try:

                # =========================================
                # FINAL FILE MOVE OPERATION
                # =========================================
                shutil.move(path, destination_path)

                print(f"- Moved: {filename}")
                global found
                found = 1

            except Exception as e:

                # =========================================
                # FILE MOVE ERROR HANDLING
                # =========================================
                print(f"Error moving {filename}: {e}")


if __name__ == "__main__":
    main()
from pathlib import Path
import argparse
import sys
import os
import re

def check_path_exists(path:str, create=False):
    '''
    Check wether path exists or not.
    If path do not exist but create=True,
    directory is created.
    '''
    if os.path.exists(path):
        return True

    #path do not exist, try to create it
    if create:
        try:
            os.makedirs(path)
            return True
        except OSError as e:
            print(f"Failed to create directory: {path}")
            print(f"Error: {e}")
    return False

def exe_helper():
    path, recursive = None, None
    while True:
        path = input("Enter the path to the folder containing the content to rename: ")
        if not check_path_exists(path):
            print("The path you entered isn't a valid path to a folder. Please re-enter the path: ")
            continue
        else:
            break
    while True:
        recursive = input("Do you want to recusivly rename files in subfolders [y/n]: ")
        if recursive not in ["y", "Y", "j", "J", "yes", "Yes", "n", "N", "no", "No"]:
            print("Type 'y' to enable recursive mode, otherwise enter 'n': ")
            continue
        elif recursive in ["y", "Y", "j", "J", "yes", "Yes"]:
            recursive = True
            break
        elif recursive in ["n", "N", "no", "No"]:
            recursive = False
            break
    return path, recursive

def rename_file(file):
    pattern = r"EPORNER\.COM - \[.*\]\s"
    directory, filename = os.path.split(file)
    if re.search(pattern, filename):
        new_filename = re.sub(pattern, "", filename)
        try:
            os.rename(os.path.join(directory,filename), os.path.join(directory,new_filename))
            print(f"Successfully renamed '{filename}' to '{new_filename}'.", flush=True)
            return
        except FileNotFoundError:
            print(f"Error: File '{file}' not found.", flush=True)
        except FileExistsError:
            print(f"Error: File '{new_filename}' already exists.", flush=True)

def get_folder_items(folder_path):
    try:
        # List all items in the folder
        items = os.listdir(folder_path)
        return items
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")

def item_itterator(folder_path, items, recursive:bool):
    for item in items:
        item_path = os.path.join(folder_path, item)

        # Check if it's a file
        if os.path.isfile(item_path):
            rename_file(item_path)
        # Check if it's a folder
        elif os.path.isdir(item_path) and recursive:
            print(f"Entering: {item_path}")
            item_itterator(item_path, get_folder_items(item_path), recursive) #Here multithreading could be implemented
            print(f"Returning into: {folder_path}")

def main():
    parser = argparse.ArgumentParser(prog='Eporner-Sanitizer', description='Remove unwanted Tags in filenames of eporner.com', epilog='https://github.com/vanishedbydefa')
    parser.add_argument('-p', '--path', default=str(os.getcwd()), type=str, help='Path to store downloaded images')
    parser.add_argument('-r', '--recursive', action='store_true', help='Specify to recursively rename all files, even if they are in a folder inside the give one.')

    args = parser.parse_args()
    folder_path = args.path       
    recursive = args.recursive

    # Check if running as exe
    exe = False
    if  getattr(sys, 'frozen', False):
        exe = True

    if exe:
        folder_path, recursive = exe_helper()

    print("Starting sanitization")
    items = get_folder_items(folder_path)
    item_itterator(folder_path, items, recursive)
    print("Sanitization done")

    if exe:
        os.system("pause")
main()

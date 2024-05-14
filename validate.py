import os
import sys
import argparse

# PyInstaller check
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

from validate_mystery import validate_mystery
from validate_event import validate_event
from validate_enemy import validate_enemy

def validate(basename, root, subdir="", print_prefix="", print_info=True):

    basename = basename.replace('\\', os.sep).replace('/', os.sep)
    root = root.replace('\\', os.sep).replace('/', os.sep)
    filepath = os.path.join(root, basename).replace('\\', os.sep)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            if line == '[mystery]':
                print(f"Recognized mystery file")
                validate_mystery(basename, root, subdir, None, None, print_prefix, print_info)
            elif line == '[event]':
                print(f"Recognized event file")
                validate_event(basename, root, subdir, None, None, print_prefix, print_info)
            elif line == '[enemy]':
                print(f"Recognized enemy file")
                validate_enemy(basename, root, subdir, None, None, print_prefix, print_info)
            else:
                print(f"Unrecognized file type")
        return True, ""
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Validate a mystery/event/enemy file.')
    parser.add_argument('path', type=str, help='Path to the .ito file')
    parser.add_argument('--subdir', type=str, default="", help='Optional subdirectory for assets and triggers (e.g. \"mystery\\")')

    args = parser.parse_args()

    filename = args.path
    subdir = args.subdir if args.subdir else "mystery" + os.sep

    valid, valid_message = validate(os.path.basename(filename), os.path.dirname(filename), subdir)
    if not valid:
        print(valid_message)

if __name__ == "__main__":
    main()
    input("Press any key to exit...")

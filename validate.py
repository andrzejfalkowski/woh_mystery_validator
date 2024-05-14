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

os.system("")
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
DARK_GRAY = '\033[90m'
RESET = '\033[0m'

def validate(ito_filepath, mod_dir="", mod_root="", print_prefix="", print_info=True):

    basename = os.path.basename(ito_filepath)
    
    try:
        with open(ito_filepath, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            if line == '[mystery]':
                print(f"Recognized mystery file")
                validate_mystery(ito_filepath, mod_dir, mod_root, None, None, print_prefix, print_info)
            elif line == '[event]':
                print(f"Recognized event file")
                validate_event(ito_filepath, mod_dir, mod_root, None, None, print_prefix, print_info)
            elif line == '[enemy]':
                print(f"Recognized enemy file")
                validate_enemy(ito_filepath, mod_dir, mod_root, None, None, print_prefix, print_info)
            else:
                print(f"Unrecognized file type")
        return True, ""
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Validate a mystery/event/enemy file.')
    parser.add_argument('ito_filepath', type=str, help='Path to the event .ito file')
    parser.add_argument('--mod_dir', type=str, default="", help='Optional directory for mods of specific type, relative to WoH .exe location, e.g. "mystery\"')
    parser.add_argument('--mod_root', type=str, default="", help='Optional directory from which paths will be built, defaults to .ito location')
    
    args = parser.parse_args()

    ito_filepath = args.ito_filepath
    mod_dir = args.mod_dir if args.mod_dir else "mystery" + os.sep
    mod_root = args.mod_root if args.mod_root else os.path.dirname(ito_filepath)
    
    ito_filepath = ito_filepath.replace('\\', os.sep).replace('/', os.sep)
    mod_dir = mod_dir.replace('\\', os.sep).replace('/', os.sep)
    mod_root = mod_root.replace('\\', os.sep).replace('/', os.sep)
    
    valid, valid_message = validate(ito_filepath, mod_dir, mod_root)
    if not valid:
        print(f"{RED}{valid_message}{RESET}")

if __name__ == "__main__":
    main()
    input("Press any key to exit...")

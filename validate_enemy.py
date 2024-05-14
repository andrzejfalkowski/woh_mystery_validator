import os
import sys
import argparse

# PyInstaller check
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(application_path, 'config')
SCRIPTS_PATH = os.path.join(application_path, 'scripts')

sys.path.append(CONFIG_PATH)
sys.path.append(SCRIPTS_PATH)

from check_quotes import check_quotes
from check_no_duplicate_keys import check_no_duplicate_keys
from check_asset_references import check_asset_references
from check_keys_and_values import check_keys_and_values
from check_keys_and_values import check_key_and_values
from check_prizes import check_prizes

ASSET_KEYS = "enemy_asset_keys.txt"
ALLOWED_DUPLICATE_KEYS = "enemy_allowed_duplicate_keys.txt"

LOCATION_KEYS = "location_keys.txt"
LOCATION_VALUES = "location_values.txt"
WEAKNESS_KEYS = "weakness_keys.txt"
WEAKNESS_VALUES = "weakness_values.txt"
ENMTYPE_KEYS = "enmtype_keys.txt"
ENMTYPE_VALUES = "enmtype_values.txt"
DAMAGETYPE_KEYS = "damagetype_keys.txt"
DAMAGETYPE_VALUES = "damagetype_values.txt"
DAMAGETYPE_KEYS = "damagetype_keys.txt"

PRIZE_NAME = "prize_name"
ITEM_VALUES = "item_values.txt"

def validate_enemy(basename, root, subdir, already_checked_events=None, already_checked_enemies=None, print_prefix="", print_info=True):

    basename = basename.replace('\\', os.sep).replace('/', os.sep)
    root = root.replace('\\', os.sep).replace('/', os.sep)
    filepath = os.path.join(root, basename).replace('\\', os.sep)
    
    os.system("")
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'
    DARK_GRAY = '\033[90m'

    if already_checked_events is None:
        already_checked_events = set()

    if already_checked_enemies is None:
        already_checked_enemies = set()
        
    if filepath in already_checked_enemies:
        print(f"{DARK_GRAY}{print_prefix}Skipping already checked enemy file: {filename}{RESET}")
        return True, "" 

    already_checked_enemies.add(filepath)        

    # Check for unclosed quotes
    if print_info:
        print(f"{print_prefix}Checking quotes...")
    quotes_valid, quotes_message = check_quotes(filepath)
    if not quotes_valid:
        print(f"{RED}{print_prefix}{quotes_message}{RESET}")
        return False, f"{basename}: {quotes_message}"
    elif print_info:
        print(f"{print_prefix}{quotes_message}")

    # Check for no duplicate keys, except allowed ones
    if print_info:
        print(f"{print_prefix}Checking key duplicates...")
    duplicates_valid, duplicates_message = check_no_duplicate_keys(filepath, os.path.join(CONFIG_PATH, ALLOWED_DUPLICATE_KEYS))
    if not duplicates_valid:
        print(f"{RED}{print_prefix}{duplicates_message}{RESET}")
        return False, f"{basename}: {quotes_message}"
    elif print_info:
        print(f"{print_prefix}{duplicates_message}")

    # Check if key values are valid
    # TODO: refactor to limit copypasta
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, WEAKNESS_KEYS), os.path.join(CONFIG_PATH, WEAKNESS_VALUES))  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, LOCATION_KEYS), os.path.join(CONFIG_PATH, LOCATION_VALUES), False)  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, ENMTYPE_KEYS), os.path.join(CONFIG_PATH, ENMTYPE_VALUES), False)  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, DAMAGETYPE_KEYS), os.path.join(CONFIG_PATH, DAMAGETYPE_VALUES), False)  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    # Only items are supported as drops for now
    keys_and_values_valid, keys_and_values_message = check_key_and_values(filepath, PRIZE_NAME, os.path.join(CONFIG_PATH, ITEM_VALUES))
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
        
    if print_info:
        print(f"{print_prefix}All keys and values validated.")

    # Check referenced files
    if print_info:
        print(f"{print_prefix}Checking file references...")
    file_ref_valid, file_ref_message = check_asset_references(basename, root, subdir, os.path.join(CONFIG_PATH, ASSET_KEYS))
    if not file_ref_valid:
        for message in file_ref_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {file_ref_message}"
    elif print_info:
        print(f"{print_prefix}{file_ref_message}")

    print(f"{GREEN}{print_prefix}{basename} enemy validation passed.{RESET}")

    return True, ""

def main():
    parser = argparse.ArgumentParser(description='Validate an enemy file.')
    parser.add_argument('path', type=str, help='Path to the enemy .ito file')
    parser.add_argument('--subdir', type=str, default="", help='Optional subdirectory for assets and triggers (e.g. \"mystery\\")')

    args = parser.parse_args()

    filename = args.path
    subdir = args.subdir

    valid, valid_message = validate_enemy(os.path.basename(filename), os.path.dirname(filename), subdir)
    if not valid:
        print(valid_message)

if __name__ == "__main__":
    main()
    input("Press any key to exit...")  

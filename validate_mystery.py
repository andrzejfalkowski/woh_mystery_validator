import os
import sys

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
from check_music_references import check_music_references
from validate_event import validate_event

ASSET_KEYS = "mystery_asset_keys.txt"
TRIGGER_KEYS = "mystery_trigger_keys.txt"
ALLOWED_DUPLICATE_KEYS = "mystery_allowed_duplicate_keys.txt"
ADDITIONAL_PREFIX = "   "

MUSIC_KEYS = "music_keys.txt"
MUSIC_VALUES = "music_values.txt"

def load_subdir_requirements(filepath):
    keys_requiring_subdirs = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0].strip()
            requires_subdir = parts[1].strip() if len(parts) > 1 else None
            keys_requiring_subdirs[key] = requires_subdir == 'True'
    return keys_requiring_subdirs

def validate_mystery(basename, root, subdir="", already_checked_events=None, already_checked_enemies=None, print_prefix="", print_info=True):

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

    triggers_requiring_subdirs = load_subdir_requirements(os.path.join(CONFIG_PATH, TRIGGER_KEYS))

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
        return False, f"{basename}: {duplicates_message}"
    elif print_info:
        print(f"{print_prefix}{duplicates_message}")

    # Check referenced assets
    if print_info:
        print(f"{print_prefix}Checking asset references...")
    file_ref_valid, file_ref_message = check_asset_references(basename, root, subdir, os.path.join(CONFIG_PATH, ASSET_KEYS), True)
    if not file_ref_valid:
        for message in file_ref_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, file_ref_message
    elif print_info:
        print(f"{print_prefix}{file_ref_message}")

    # Check referenced music (can use hardcoded values)
    if print_info:
        print(f"{print_prefix}Checking music references...")
    music_ref_valid, music_ref_message = check_music_references(basename, root, subdir, os.path.join(CONFIG_PATH, MUSIC_KEYS), os.path.join(CONFIG_PATH, MUSIC_VALUES), True)
    if not music_ref_valid:
        for message in music_ref_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, music_ref_message
    elif print_info:
        print(f"{print_prefix}{music_ref_message}")

    # Check _frc triggers
    if print_info:
        print(f"{print_prefix}Checking forced events...")
    with open(filepath, 'r') as file:
        for line in file:
            if '_frc="' in line:
                key, path = line.split('=', 1)
                key = key.strip()
                path = path.strip().strip('"').replace('\\', os.sep).replace('/', os.sep)
                if path:
                    if key in triggers_requiring_subdirs and triggers_requiring_subdirs[key] and path.startswith(subdir):
                        path = path[len(subdir):]
                    full_path = os.path.join(root, path)
                    if print_info:
                        print(f"{print_prefix}Checking referenced event file: {path} {full_path}")
                    if not os.path.exists(full_path):
                        print(f"{RED}{print_prefix}Referenced file {path} does not exist.{RESET}")
                        return False, f"{basename}: Referenced file {path} does not exist."
                    if print_info:
                        print(f"{print_prefix}Validating linked event file: {path}")
                    linked_event_valid, linked_event_message = validate_event(path, root, subdir, already_checked_events, already_checked_enemies, print_prefix + ADDITIONAL_PREFIX, print_info)
                    if not linked_event_valid:
                        return False, f"{linked_event_message}"

    if len(already_checked_enemies) > 0:
        print(f"Validated {len(already_checked_enemies)} enemies:")
        for enemy in already_checked_enemies:
            print(f"{ADDITIONAL_PREFIX}{os.path.basename(enemy)}")

    if len(already_checked_events) > 0:
        print(f"Validated {len(already_checked_events)} events:")
        for event in already_checked_events:
            print(f"{ADDITIONAL_PREFIX}{os.path.basename(event)}")

    print(f"{GREEN}{basename} mystery validation passed.{RESET}")

    return True, ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_mystery.py <path_to_mystery_ito_file>")
    else:
        filename = sys.argv[1]
        valid, valid_message = validate_mystery(os.path.basename(filename), os.path.dirname(filename), "mystery" + os.sep)
        if not valid:
            print(valid_message)
        input("Press any key to exit...")

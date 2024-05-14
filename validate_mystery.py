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
from check_music_references import check_music_references
from validate_event import validate_event

ASSET_KEYS = "mystery_asset_keys.txt"
TRIGGER_KEYS = "mystery_trigger_keys.txt"
ALLOWED_DUPLICATE_KEYS = "mystery_allowed_duplicate_keys.txt"
ADDITIONAL_PREFIX = "   "

MUSIC_KEYS = "music_keys.txt"
MUSIC_VALUES = "music_values.txt"

os.system("")
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
DARK_GRAY = '\033[90m'
RESET = '\033[0m'

def load_mod_dir_requirements(filepath):
    keys_requiring_mod_dir = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0].strip()
            requires_subdir = parts[1].strip() if len(parts) > 1 else None
            keys_requiring_mod_dir[key] = requires_subdir == 'True'
    return keys_requiring_mod_dir

# ito_filepath - path to .ito file, relative to script location
# mos_dir - subdirectory for specific mod type, would be relative to WoH .exe location, e.g. "mystery\", some asset paths require it to be specified, some don't, even inside the same file, complete clown show
# mod_root - path to main directory of the mod, can be relative to script location, by default same directory as ito_filepath, but might be overriden when e.g. validiating msytery events from subdirectory directly
def validate_mystery(ito_filepath, mod_dir="", mod_root="", already_checked_events=None, already_checked_enemies=None, print_prefix="", print_info=True):

    basename = os.path.basename(ito_filepath)

    if already_checked_events is None:
        already_checked_events = set()

    if already_checked_enemies is None:
        already_checked_enemies = set()

    triggers_requiring_mod_dir = load_mod_dir_requirements(os.path.join(CONFIG_PATH, TRIGGER_KEYS))

    # Check for unclosed quotes
    if print_info:
        print(f"{print_prefix}Checking quotes...")
    quotes_valid, quotes_message = check_quotes(ito_filepath)
    if not quotes_valid:
        print(f"{RED}{print_prefix}{quotes_message}{RESET}")
        return False, f"{basename}: {quotes_message}"
    elif print_info:
        print(f"{print_prefix}{quotes_message}")

    # Check for no duplicate keys, except allowed ones
    if print_info:
        print(f"{print_prefix}Checking key duplicates...")
    duplicates_valid, duplicates_message = check_no_duplicate_keys(ito_filepath, os.path.join(CONFIG_PATH, ALLOWED_DUPLICATE_KEYS))
    if not duplicates_valid:
        print(f"{RED}{print_prefix}{duplicates_message}{RESET}")
        return False, f"{basename}: {duplicates_message}"
    elif print_info:
        print(f"{print_prefix}{duplicates_message}")

    # Check referenced assets
    if print_info:
        print(f"{print_prefix}Checking asset references...")
    file_ref_valid, file_ref_message = check_asset_references(ito_filepath, mod_dir, mod_root, os.path.join(CONFIG_PATH, ASSET_KEYS), True)
    if not file_ref_valid:
        for message in file_ref_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, file_ref_message
    elif print_info:
        print(f"{print_prefix}{file_ref_message}")
    
    # Check referenced music (can use hardcoded values)
    if print_info:
        print(f"{print_prefix}Checking music references...")
    music_ref_valid, music_ref_message = check_music_references(ito_filepath, mod_dir, mod_root, os.path.join(CONFIG_PATH, MUSIC_KEYS), os.path.join(CONFIG_PATH, MUSIC_VALUES), True)
    if not music_ref_valid:
        for message in music_ref_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, music_ref_message
    elif print_info:
        print(f"{print_prefix}{music_ref_message}")
        

    # Check _frc triggers
    if print_info:
        print(f"{print_prefix}Checking forced events...")
    with open(ito_filepath, 'r') as file:
        for line in file:
            if '_frc="' in line:
                key, path = line.split('=', 1)
                key = key.strip()
                path = path.strip().strip('"').replace('\\', os.sep).replace('/', os.sep)
                if path:
                    if key in triggers_requiring_mod_dir and triggers_requiring_mod_dir[key] and path.startswith(mod_dir):
                        path = path[len(mod_dir):]
                    ref_full_path = os.path.join(mod_root, path)
                    if print_info:
                        print(f"{print_prefix}Checking referenced event file: {path}")
                    if not os.path.exists(ref_full_path):
                        print(f"{RED}{print_prefix}Referenced file {path} does not exist.{RESET}")
                        return False, f"{basename}: Referenced file {path} does not exist."
                    if print_info:
                        print(f"{print_prefix}Validating linked event file: {path}")
                    linked_event_valid, linked_event_message = validate_event(ref_full_path, mod_dir, mod_root, already_checked_events, already_checked_enemies, print_prefix + ADDITIONAL_PREFIX, print_info)
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

    print(f"{GREEN}{print_prefix}{basename} mystery validation passed.{RESET}")

    return True, f"{basename} mystery validation passed."

def main():
    parser = argparse.ArgumentParser(description='Validate a mystery file.')
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
    
    valid, valid_message = validate_mystery(ito_filepath, mod_dir, mod_root)
    if not valid:
        print(f"{RED}{valid_message}{RESET}")

if __name__ == "__main__":
    main()
    input("Press any key to exit...")

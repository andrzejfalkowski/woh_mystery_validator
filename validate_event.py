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
from check_trigger_references import check_trigger_references
from check_keys_and_values import check_keys_and_values
from check_prizes import check_prizes
from validate_enemy import validate_enemy

ASSET_KEYS = "event_asset_keys.txt"
TRIGGER_KEYS = "event_trigger_keys.txt"
ALLOWED_DUPLICATE_KEYS = "event_allowed_duplicate_keys.txt"

ITEM_PRIZE_TYPE = "item"
ITEM_VALUES = "item_values.txt"
ITEMPOOL_PRIZE_TYPE = "itempool"
ITEMPOOL_VALUES = "itempool_values.txt"
CURSE_EX_PRIZE_TYPE = "curse_ex"
CURSE_EX_VALUES = "curse_ex_values.txt"
SPELL_EX_PRIZE_TYPE = "spell_ex"
SPELL_EX_VALUES = "spell_ex_values.txt"
INJURY_EX_PRIZE_TYPE = "injury_ex"
INJURY_EX_VALUES = "injury_ex_values.txt"
ALLY_EX_PRIZE_TYPE = "ally_ex"
ALLY_EX_VALUES = "ally_ex_values.txt"
CARD_ADD_PRIZE_TYPE = "card_add"
CARD_ADD_VALUES = "card_add_values.txt"

WINPRIZE_KEYS = "winprize_keys.txt"
WINPRIZE_VALUES = "winprize_values.txt"
EXTRA_WINPRIZE_KEYS = "extra_winprize_keys.txt"
EXTRA_WINPRIZE_VALUES = "extra_winprize_values.txt"
WINEFFECT_KEYS = "wineffect_keys.txt"
WINEFFECT_VALUES = "wineffect_values.txt"

LOCATION_KEYS = "location_keys.txt"
LOCATION_VALUES = "location_values.txt"
CHARACTER_KEYS = "character_keys.txt"
CHARACTER_VALUES = "character_values.txt"

ADDITIONAL_PREFIX = "   "

def load_exclusions(filepath):
    exclusions = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0].strip()
            exclusion = parts[1].strip() + os.sep if len(parts) > 1 else None
            exclusions[key] = exclusion
    return exclusions

def validate_event(basename, root, already_checked_events=None, already_checked_enemies=None, print_prefix="", print_info=True):

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
        
    if filepath in already_checked_events:
        print(f"{DARK_GRAY}{print_prefix}Skipping already checked event file: {basename}{RESET}")
        return True, "" 
        
    already_checked_events.add(filepath)
        
    filepath_exclusions = load_exclusions(os.path.join(CONFIG_PATH, ASSET_KEYS))
    trigger_path_exclusions = load_exclusions(os.path.join(CONFIG_PATH, TRIGGER_KEYS))

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
    if print_info:
        print(f"{print_prefix}Checking keys and valid values...")
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, WINPRIZE_KEYS), os.path.join(CONFIG_PATH, WINPRIZE_VALUES))  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, EXTRA_WINPRIZE_KEYS), os.path.join(CONFIG_PATH, EXTRA_WINPRIZE_VALUES))  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, WINEFFECT_KEYS), os.path.join(CONFIG_PATH, WINEFFECT_VALUES))  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, LOCATION_KEYS), os.path.join(CONFIG_PATH, LOCATION_VALUES))  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
    keys_and_values_valid, keys_and_values_message = check_keys_and_values(filepath, os.path.join(CONFIG_PATH, CHARACTER_KEYS), os.path.join(CONFIG_PATH, CHARACTER_VALUES))  
    if not keys_and_values_valid:
        for message in keys_and_values_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {keys_and_values_message}"
        
    if print_info:
        print(f"{print_prefix}All keys and values validated.")
        
    # Check prizes - acceptable prize values depend on prize types
    # TODO: refactor to dictionary of prize types and value configs instead of each pair hardcoded
    if print_info:
        print(f"{print_prefix}Checking prizes...")
    prizes_valid, prizes_message = check_prizes(filepath, ITEM_PRIZE_TYPE, os.path.join(CONFIG_PATH, ITEM_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    prizes_valid, prizes_message = check_prizes(filepath, ITEMPOOL_PRIZE_TYPE, os.path.join(CONFIG_PATH, ITEMPOOL_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    prizes_valid, prizes_message = check_prizes(filepath, CURSE_EX_PRIZE_TYPE, os.path.join(CONFIG_PATH, CURSE_EX_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    prizes_valid, prizes_message = check_prizes(filepath, SPELL_EX_PRIZE_TYPE, os.path.join(CONFIG_PATH, SPELL_EX_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    prizes_valid, prizes_message = check_prizes(filepath, INJURY_EX_PRIZE_TYPE, os.path.join(CONFIG_PATH, INJURY_EX_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    prizes_valid, prizes_message = check_prizes(filepath, ALLY_EX_PRIZE_TYPE, os.path.join(CONFIG_PATH, ALLY_EX_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    prizes_valid, prizes_message = check_prizes(filepath, CARD_ADD_PRIZE_TYPE, os.path.join(CONFIG_PATH, CARD_ADD_VALUES)) 
    if not prizes_valid:
        for message in prizes_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {prizes_message}"
    
    if print_info:
        print(f"{print_prefix}All prizes validated.")
    
    # Check referenced files
    if print_info:
        print(f"{print_prefix}Checking file references...")
    file_ref_valid, file_ref_message = check_asset_references(basename, root, os.path.join(CONFIG_PATH, ASSET_KEYS))
    if not file_ref_valid:
        for message in file_ref_message:
            print(f"{print_prefix}{RED}{message}{RESET}")
        return False, f"{basename}: {file_ref_message}"
    elif print_info:
        print(f"{print_prefix}{file_ref_message}")
        
    # Conditional trigger reference check
    trigger_ref_valid, trigger_ref_message = check_trigger_references(basename, root, os.path.join(CONFIG_PATH, TRIGGER_KEYS))
    if not trigger_ref_valid:
        for message in trigger_ref_message:
            print(f"{print_prefix}{message}")
        return False, f"{basename}: {trigger_ref_message}"

    print(f"{GREEN}{print_prefix}{basename} event validation passed.{RESET}")

    events_to_check = {}
    enemies_to_check = {}
    prize_conditions = {}

    with open(filepath, 'r') as file:
        for line in file:
            if 'winprize' in line:
                key, value = line.split('=', 1)
                prize_conditions[key.strip()] = value.strip().strip('"')
            elif 'winnumber' in line:
                key, path = line.split('=', 1)
                key = key.strip()
                path = path.strip().strip('"')
                condition_key = key.replace('number', 'prize')
                # Check if the corresponding prize key indicates a file path needs checking
                if prize_conditions.get(condition_key) == "trigger_event":
                    if path:  # Ensure non-empty path
                        events_to_check[key] = path
                if prize_conditions.get(condition_key) == "trigger_enemy":
                    if path:  # Ensure non-empty path
                        enemies_to_check[key] = path
            elif 'failprize' in line:
                key, value = line.split('=', 1)
                prize_conditions[key.strip()] = value.strip().strip('"')
            elif 'failnumber' in line:
                key, path = line.split('=', 1)
                key = key.strip()
                path = path.strip().strip('"')
                condition_key = key.replace('number', 'prize')
                # Check if the corresponding prize key indicates a file path needs checking
                if prize_conditions.get(condition_key) == "trigger_event":
                    if path:  # Ensure non-empty path
                        events_to_check[key] = path
                if prize_conditions.get(condition_key) == "trigger_enemy":
                    if path:  # Ensure non-empty path
                        enemies_to_check[key] = path

    # Validate each linked enemy
    for key, path in enemies_to_check.items():
        if key in trigger_path_exclusions and trigger_path_exclusions[key] and path.startswith(trigger_path_exclusions[key]):
            path = path[len(trigger_path_exclusions[key]):]
        path = path.replace('\\', os.sep)
        full_path = os.path.join(root, path)
        if not os.path.exists(full_path):
            print(f"{RED}{print_prefix}Referenced file {path} does not exist.{RESET}")
            return False, f"{basename}: Referenced file {path} does not exist."
        file_ref_valid, file_ref_message
        if print_info:
            print(f"{print_prefix}Validating linked enemy file: {path}")
        linked_enemy_valid, linked_enemy_message = validate_enemy(path, root, already_checked_events, already_checked_enemies, print_prefix + ADDITIONAL_PREFIX, print_info)
        if not linked_enemy_valid:
            return False, f"{linked_enemy_message}"
 
    # Recursively validate each linked event
    for key, path in events_to_check.items():
        if key in trigger_path_exclusions and trigger_path_exclusions[key] and path.startswith(trigger_path_exclusions[key]):
            path = path[len(trigger_path_exclusions[key]):]
        path = path.replace('\\', os.sep)
        full_path = os.path.join(root, path)
        if not os.path.exists(full_path):
            print(f"{RED}{print_prefix}Referenced file {path} does not exist.{RESET}")
            return False, f"{filename}: Referenced file {path} does not exist."
        file_ref_valid, file_ref_message
        if print_info:
            print(f"{print_prefix}Validating linked event file: {path}")
        linked_event_valid, linked_event_message = validate_event(path, root, already_checked_events, already_checked_enemies, print_prefix + "   ", print_info)
        if not linked_event_valid:
            return False, f"{linked_event_message}"

    return True, ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_event.py <path_to_event_ito_file>")
    else:
        filename = sys.argv[1]
        valid, valid_message = validate_event(os.path.basename(filename), os.path.dirname(filename))
        if not valid:
            print(valid_message)
        
import os

def load_subdir_requirements(filepath):
    keys_requiring_subdirs = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0].strip()
            requires_subdir = parts[1].strip() if len(parts) > 1 else None
            keys_requiring_subdirs[key] = requires_subdir == 'True'
    return keys_requiring_subdirs
        
# Check if referenced events exist
def check_trigger_references(basename, root, keys_file, allow_n_r = False):
 
    triggers_requiring_subdirs = load_subdir_requirements(keys_file)

    basename = basename.replace('\\', os.sep).replace('/', os.sep)
    root = root.replace('\\', os.sep).replace('/', os.sep)
    filepath = os.path.join(root, basename).replace('\\', os.sep)

    try:
        prizes = {}
        filepaths = {}
        
        with open(filepath, 'r', encoding='utf-8') as file:
            errors = []
            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').replace('\\', os.sep).replace('/', os.sep)

                    # Triggers can only be set as a prize
                    if 'winprize' in key:
                        prizes[key] = value
                    elif 'winnumber' in key:
                        filepaths[key] = value
                    elif 'failprize' in key:
                        prizes[key] = value
                    elif 'failnumber' in key:
                        filepaths[key] = value

            for key, value in filepaths.items():
                prize_key = key.replace('number', 'prize')
                
                if prizes.get(prize_key) == "trigger_event":
                    if key in triggers_requiring_subdirs and value:
                        if triggers_requiring_subdirs[key]:
                            if not value.startswith(subdir):
                                errors.append(f"Missing required root '{subdir}' for key '{key}'. Found '{value}'.")
                                continue
                            value = value[len(subdir):]

                        ref_full_path = os.path.join(root, value)
                        if not os.path.exists(ref_full_path):
                            errors.append(f"File not found: {value} referenced at key '{key}'")
                        else:
                            # Special rule - check if the filename starts with 'n' or 'r'
                            ref_filename = os.path.basename(ref_full_path)
                            if ref_filename[0].lower() in ['n', 'r'] and not allow_n_r:
                                errors.append(f"Filename '{ref_filename}' starts with restricted character 'n' or 'r' at key '{key}'")
        if errors:
            return False, errors
        return True, f"All triggers validated."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

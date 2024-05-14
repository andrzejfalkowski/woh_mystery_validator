import os

def load_keys_and_roots(filepath):
    keys_and_roots = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    key = parts[0].strip()
                    required_path = parts[1].strip() + os.sep if len(parts) > 1 else None
                    keys_and_roots[key] = required_path
        return keys_and_roots
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Configuration file '{filepath}' not found. Please ensure the file exists to continue.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the key paths file: {str(e)}")
        
# Check if referenced events exist
def check_trigger_references(basename, root, keys_file, allow_n_r = False):
 
    keys_and_roots = load_keys_and_roots(keys_file)

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
                    if key in keys_and_roots and value:
                        required_path = keys_and_roots[key]
                        if required_path:
                            if not value.startswith(required_path):
                                errors.append(f"Missing required root '{required_path}' for key '{key}'. Found '{value}'.")
                                continue
                            value = value[len(required_path):]

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

import os

def load_mod_dir_requirements(filepath):
    keys_requiring_mod_dir = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0].strip()
            requires_mod_dir = parts[1].strip() if len(parts) > 1 else None
            keys_requiring_mod_dir[key] = requires_mod_dir == 'True'
    return keys_requiring_mod_dir
        
# Check if referenced events exist
def check_trigger_references(ito_filepath, mod_dir, mod_root, keys_file, allow_n_r = False):
 
    triggers_requiring_mod_dir = load_mod_dir_requirements(keys_file)

    try:
        prizes = {}
        filepaths = {}
        
        with open(ito_filepath, 'r', encoding='utf-8') as file:
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
                    if key in triggers_requiring_mod_dir and value:
                        if mod_dir and triggers_requiring_mod_dir[key]:
                            if not value.startswith(mod_dir):
                                errors.append(f"Missing required mod_dir '{mod_dir}' for key '{key}'. Found '{value}'.")
                                continue
                            value = value[len(mod_dir):]

                        ref_full_path = os.path.join(mod_root, value)
                        if not os.path.exists(ref_full_path):
                            errors.append(f"File not found: {value} ({ref_full_path}) referenced at key '{key}'")
                        else:
                            # Special rule - check if the filename starts with 'n' or 'r'
                            ref_basename = os.path.basename(ref_full_path)
                            if ref_basename[0].lower() in ['n', 'r'] and not allow_n_r:
                                    errors.append(f"Filename '{ref_basename}' starts with restricted character 'n' or 'r' at key '{key}'")  
        if errors:
            return False, errors
        return True, f"All triggers validated."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

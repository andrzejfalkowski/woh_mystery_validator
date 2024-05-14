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

# Check if referenced files exist for specified keys
def check_asset_references(basename, root, keys_file, allow_n_r = False):

    keys_and_roots = load_keys_and_roots(keys_file)

    basename = basename.replace('\\', os.sep).replace('/', os.sep)
    root = root.replace('\\', os.sep).replace('/', os.sep)
    filepath = os.path.join(root, basename).replace('\\', os.sep)

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            errors = []
            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').replace('\\', os.sep).replace('/', os.sep)
                    if key in keys_and_roots and value:  # Only proceed if value is not empty
                        required_path = keys_and_roots[key]
                        if required_path:
                            if not value.startswith(required_path):
                                errors.append(f"Missing required root '{required_path}' for key '{key}'. Found '{value}'.")
                                continue
                            # Exclude root
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
            return True, f"All file references are valid."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

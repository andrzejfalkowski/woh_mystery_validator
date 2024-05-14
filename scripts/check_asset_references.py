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

# Check if referenced files exist for specified keys
def check_asset_references(basename, root, subdir, keys_file, allow_n_r = False):

    assets_requiring_subdirs = load_subdir_requirements(keys_file)

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
                    if key in assets_requiring_subdirs and value:  # Only proceed if value is not empty
                        if assets_requiring_subdirs[key]:
                            if not value.startswith(subdir):
                                errors.append(f"Missing required root '{subdir}' for key '{key}'. Found '{value}'.")
                                continue
                            # Exclude root
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
            return True, f"All file references are valid."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

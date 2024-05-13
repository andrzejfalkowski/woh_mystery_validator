def load_allowed_duplicates(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            allowed_duplicates = [line.strip() for line in file if line.strip()]
        return allowed_duplicates
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Allowed duplicates configuration file '{filepath}' not found. Please ensure the file exists to continue.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the allowed duplicates file: {str(e)}")

def check_no_duplicate_keys(filepath, allowed_duplicates_file):

    allowed_duplicates = load_allowed_duplicates(allowed_duplicates_file)

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            seen_keys = {}
            line_number = 0
            for line in file:
                line_number += 1
                line = line.strip()
                if '=' in line:
                    key = line.split('=')[0].strip()
                    if key in seen_keys and key not in allowed_duplicates:
                        return False, f"Duplicate key '{key}' found at line {line_number}"
                    seen_keys[key] = line_number
                elif line.startswith('[') and line.endswith(']'):
                    key = line
                    if key in seen_keys:
                        return False, f"Duplicate section '{key}' found at line {line_number}"
                    seen_keys[key] = line_number

        return True, "No duplicate keys found."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

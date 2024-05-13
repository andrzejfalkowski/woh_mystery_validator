import os

def load_valid_keys(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Configuration file '{filepath}' not found. Please ensure the file exists to continue.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the hardcoded values file: {str(e)}")

def load_valid_values(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Configuration file '{filepath}' not found. Please ensure the file exists to continue.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the hardcoded values file: {str(e)}")

def check_key_and_values(filepath, key_to_check, values_file, allow_empty=True):

    valid_values = load_valid_values(values_file)

    try: 
        with open(filepath, 'r', encoding='utf-8') as file:
            errors = []

            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    
                    if key == key_to_check:
                        if (not value or value.isspace()) and allow_empty:
                            continue
                        if not value in valid_values:
                            errors.append(f"Incorrect value '{value}' for key '{key}'.")

        if errors:
            return False, errors
        return True, f"All key and values validated."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def check_keys_and_values(filepath, keys_file, values_file, allow_empty=True):

    valid_keys = load_valid_keys(keys_file)
    valid_values = load_valid_values(values_file)

    try: 
        with open(filepath, 'r', encoding='utf-8') as file:
            errors = []

            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    #print(f"{key}:{value}")
                    if key in valid_keys:
                        if (not value or value.isspace()) and allow_empty:
                            continue
                        if not value in valid_values:
                            errors.append(f"Incorrect value '{value}' for key '{key}'.")

        if errors:
            return False, errors
        return True, f"All key and values validated."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

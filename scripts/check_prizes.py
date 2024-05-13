import os

def load_valid_values(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Configuration file '{filepath}' not found. Please ensure the file exists to continue.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the hardcoded values file: {str(e)}")

# Check if correct prize is set for that prize type
def check_prizes(filepath, prize_type, values_file):
    valid_values = load_valid_values(values_file)

    try:
        prize_keys = {}
        prizes = {}
        
        with open(filepath, 'r', encoding='utf-8') as file:
            errors = []
            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"')

                    # Detect if it's a prize or number based on prefix
                    if 'winprize' in key:
                        prize_keys[key] = value
                    elif 'winnumber' in key:
                        prizes[key] = value
                    elif 'failprize' in key:
                        prize_keys[key] = value
                    elif 'failnumber' in key:
                        prizes[key] = value

            # Check if this is valid prize for that prize type
            for key, value in prizes.items():
                prize_key = key.replace('number', 'prize')
                if prize_keys.get(prize_key) == prize_type:
                    if not value in valid_values:
                        errors.append(f"Incorrect prize '{value}' for prize type '{prize_type}' at key '{key}'.")
                        continue 
        if errors:
            return False, errors
        return True, f"All prizes validated."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

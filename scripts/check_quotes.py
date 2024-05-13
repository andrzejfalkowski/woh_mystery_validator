def check_quotes(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            line_number = 0
            for line in file:
                line_number += 1
                quote_count = line.count('"')

                if quote_count % 2 != 0:
                    return False, f"Unclosed quotes found at line {line_number}"

        return True, "All quotes are correctly closed."
    except Exception as e:
        return False, f"Error: {str(e)}"
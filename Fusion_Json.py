import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def merge_alpaca_files(file1, file2, output_file):
    # Load both JSON files
    data1 = load_json(file1)
    data2 = load_json(file2)
    
    # Ensure both files contain a list of records
    if not isinstance(data1, list) or not isinstance(data2, list):
        raise ValueError("Both JSON files must contain a list of records.")
    
    # Combine the records
    merged_data = data1 + data2
    
    # Save the merged data to the output file
    save_json(merged_data, output_file)

# Example usage
file1 = "F:/LLM_Fine_Tune/bgb_alpaca_cleaned.json"
file2 = "F:/LLM_Fine_Tune/court_decisions_data_alpaca.json"
output_file = "F:/LLM_Fine_Tune/bgb_court_decisions_data_alpaca.json"

merge_alpaca_files(file1, file2, output_file)

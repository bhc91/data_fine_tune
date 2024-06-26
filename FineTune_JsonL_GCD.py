import json

# Load the JSONL data
input_file = "C:/court_decisions_data.jsonl"
output_file = "F:/LLM_Fine_Tune/court_decisions_data_alpaca.json"

# Read the JSONL file
with open(input_file, 'r', encoding='utf-8') as f:
    json_list = [json.loads(line) for line in f]

# Transform the data into Alpaca prompt format
alpaca_data = []
for entry in json_list:
    transformed_entry = {
        "instruction": entry["offense"],
        "input": "",
        "output": entry["decision"]
    }
    alpaca_data.append(transformed_entry)

# Write the transformed data to a JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(alpaca_data, f, ensure_ascii=False, indent=4)

print(f'Transformed data has been written to {output_file}')
import json

# Pfad zur ursprünglichen JSON-Datei
input_file = "F:/LLM_Fine_Tune/bgb_court_decisions_data_alpaca.json"
# Pfad zur neuen JSON-Datei
output_file = "F:/LLM_Fine_Tune/bgb_court_decisions_alpaca_third.json"

# JSON-Datei einlesen
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Berechnen des ersten Drittels
one_third_length = len(data) // 3

# Behalten des ersten Drittels
first_third_data = data[:one_third_length]

# Neue JSON-Datei speichern
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(first_third_data, file, ensure_ascii=False, indent=4)

print(f'The first third of the data was saved in {output_file}')

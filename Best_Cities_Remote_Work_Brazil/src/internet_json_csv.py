import json
import pandas as pd

# Load the JSON file
with open('C:/Users/samue/OneDrive/Documents/Data-Science-Studies/Best_Cities_Remote_Work_Brazil/src/internet_quality.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# List of state capitals in Brazil with their state codes
capitals = {
    'Rio Branco': 'AC', 'Maceio': 'AL', 'Macapa': 'AP', 'Manaus': 'AM', 'Salvador': 'BA', 'Fortaleza': 'CE',
    'Brasília': 'DF', 'Vitoria': 'ES', 'Goiania': 'GO', 'São Luis': 'MA', 'Cuiaba': 'MT', 'Campo Grande': 'MS',
    'Belo Horizonte': 'MG', 'Belem': 'PA', 'João Pessoa': 'PB', 'Curitiba': 'PR', 'Recife': 'PE', 'Teresina': 'PI',
    'Rio De Janeiro': 'RJ', 'Natal': 'RN', 'Porto Alegre': 'RS', 'Porto Velho': 'RO', 'Boa Vista': 'RR',
    'Florianópolis': 'SC', 'São Paulo': 'SP', 'Aracaju': 'SE', 'Palmas': 'TO'
}

# Filter the JSON for only capitals
capital_data = [
    entry for entry in data
    if entry['city'].strip().title() in capitals and entry['state'].strip().upper() == capitals[entry['city'].strip().title()]
]

# Convert to DataFrame
df_capitals = pd.DataFrame(capital_data)

# Optional: sort by speed
df_capitals = df_capitals.sort_values(by='speed_mbps', ascending=False)

# Save to CSV
df_capitals.to_csv('internet_quality_capitals.csv', index=False, encoding='utf-8')

# Preview
print(df_capitals)

import pandas as pd

# Load the full IPS dataset
df = pd.read_csv("C:/Users/samue/OneDrive/Documents/Data-Science-Studies/Best_Cities_Remote_Work_Brazil/data/ips_brasil_municipios.csv", encoding="utf-8")

# List of capitals as they appear in the "Município" column
capitals_with_uf = [
    "Rio Branco (AC)", "Maceió (AL)", "Macapá (AP)", "Manaus (AM)", "Salvador (BA)", "Fortaleza (CE)",
    "Brasília (DF)", "Vitória (ES)", "Goiânia (GO)", "São Luís (MA)", "Cuiabá (MT)", "Campo Grande (MS)",
    "Belo Horizonte (MG)", "Belém (PA)", "João Pessoa (PB)", "Curitiba (PR)", "Recife (PE)", "Teresina (PI)",
    "Rio de Janeiro (RJ)", "Natal (RN)", "Porto Alegre (RS)", "Porto Velho (RO)", "Boa Vista (RR)",
    "Florianópolis (SC)", "São Paulo (SP)", "Aracaju (SE)", "Palmas (TO)"
]

# Filter the DataFrame to only include capitals
capitals_df = df[df['Município'].isin(capitals_with_uf)].copy()

# Remove the "(UF)" part from the city name
capitals_df['Município'] = capitals_df['Município'].str.extract(r'^(.+?)\s*\(')[0].str.strip()

# Save to new CSV
capitals_df.to_csv("ips_capitals.csv", index=False, encoding="utf-8")

print("✔️ CSV saved as 'ips_capitals.csv' with capitals and city names cleaned")
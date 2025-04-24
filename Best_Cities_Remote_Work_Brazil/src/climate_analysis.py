import pandas as pd
import os

# List of Brazilian capital cities (lowercase with underscores)
cities = [
    "aracaju", "belem", "belo_horizonte", "boa_vista", "brasilia", "cuiaba", "curitiba",
    "florianopolis", "fortaleza", "goiania", "joao_pessoa", "macapa", "maceio", "manaus",
    "natal", "porto_alegre", "porto_velho", "rio_branco", "rio_de_janeiro", "salvador",
    "sao_luis", "sao_paulo", "teresina", "vitoria"
]

# Base path for the climate data files - change this to your local path
base_path = "C:/Users/samue/OneDrive/Documents/Data-Science-Studies/Best_Cities_Remote_Work_Brazil/data/climate_data/"

# Final summary results
summary = []

for city in cities:
    file_path = os.path.join(base_path, f"data_{city}.csv")
    
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Find where the actual data table starts
    for i, line in enumerate(lines):
        if line.startswith("Data Medicao"):
            data_start_index = i
            break

    # Read only the 4 first columns to avoid extra empty ones
    data = pd.read_csv(
        file_path,
        skiprows=data_start_index,
        sep=';',
        decimal='.',
        na_values=['null'],
        usecols=range(4)
    )

    # Rename columns to English
    data.columns = ["Date", "Precipitation_Days", "Average_Temperature", "Average_Wind_Speed"]

    # Remove rows with missing temperature or precipitation
    valid_data = data.dropna(subset=["Precipitation_Days", "Average_Temperature"])

    # Compute averages from valid data only
    avg_precip_days = valid_data["Precipitation_Days"].mean()
    avg_temperature = valid_data["Average_Temperature"].mean()

    summary.append({
        "City": city.replace("_", " ").title(),
        "Avg Precipitation Days": round(avg_precip_days, 2),
        "Avg Annual Temperature (°C)": round(avg_temperature, 2)
    })

# Create DataFrame and sort by temperature
df_summary = pd.DataFrame(summary)
df_summary.sort_values(by="Avg Annual Temperature (°C)", ascending=False, inplace=True)

# Print results to terminal
print(df_summary.to_string(index=False))

# Export to CSV
os.makedirs("data", exist_ok=True)
df_summary.to_csv("data/climate_summary.csv", index=False, encoding="utf-8-sig")
print("/nSummary saved to: data/climate_summary.csv")

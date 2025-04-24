import pandas as pd

# Read the Excel file without headers to handle merged cells
df = pd.read_excel('C:/Users/samue/OneDrive/Documents/Data-Science-Studies/Best_Cities_Remote_Work_Brazil/src/mortes_por_capital.xlsx', sheet_name='Planilha1', header=None)

# Filter rows where the UF (column 1) is not empty
filtered = df[df[1].notna() & (df[1] != '')]

# Select capital names (column 2) and 2023 Taxa (column 18)
result = filtered[[2, 18]]

# Rename columns and save to CSV
result.columns = ['Capital', 'Taxa_2023']
result.to_csv('death_per_capital_2023.csv', index=False)

print("Data saved to 'death_per_capital_2023.csv'")
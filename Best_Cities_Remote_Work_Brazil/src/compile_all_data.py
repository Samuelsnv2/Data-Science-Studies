import pandas as pd
import json
from os.path import join

def load_json_file(file_path):
    """Carrega dados de um arquivo JSON"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}

def compile_data():
    print("Compiling all data...")

    # Caminho para os arquivos JSON
    data_dir = "../data"
    
    # Carregar os arquivos JSON individuais
    cost_of_living_data = load_json_file(join(data_dir, "cost_of_living.json"))
    safety_data = load_json_file(join(data_dir, "safety_data.json"))
    climate_data = load_json_file(join(data_dir, "climate_data.json"))
    coworking_data = load_json_file(join(data_dir, "coworking_data.json"))
    transportation_data = load_json_file(join(data_dir, "transportation_data.json"))
    quality_of_life_data = load_json_file(join(data_dir, "quality_of_life.json"))

    # Preparar as listas para a criação do DataFrame
    cities = list(cost_of_living_data.keys())

    compiled_data = []
    
    for city in cities:
        compiled_data.append({
            "city": city,
            "cost_of_living": cost_of_living_data.get(city, {}).get('cost_of_living', None),
            "safety_index": safety_data.get(city, {}).get('safety_index', None),
            "climate_temp": climate_data.get(city, {}).get('temperature', None),
            "avg_coworking_price": coworking_data.get(city, {}).get('avg_coworking_price', None),
            "transportation_index": transportation_data.get(city, {}).get('transportation_index', None),
            "quality_of_life_index": quality_of_life_data.get(city, {}).get('quality_of_life_index', None),
        })
    
    # Criar o DataFrame
    df = pd.DataFrame(compiled_data)

    # Salvar o DataFrame em um arquivo CSV
    output_file = join(data_dir, "brazil_remote_work_cities.csv")
    df.to_csv(output_file, index=False)
    print(f"Consolidated data saved to {output_file}")

if __name__ == "__main__":
    compile_data()

import requests
from bs4 import BeautifulSoup
import json
from save_utils import save_json

cities = [
    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
    "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre",
    "Belém", "Goiânia", "Florianópolis", "Natal", "Vitória", "Santos"
]

# URL de exemplo (ajustar para o site desejado)
URL_TEMPLATE = "https://www.numbeo.com/crime/in/{}/"

def get_safety_data(city):
    try:
        city_formatted = city.lower().replace(" ", "-")
        url = URL_TEMPLATE.format(city_formatted)
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve data for {city}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Aqui você vai ajustar conforme a estrutura da página
        safety_index = soup.find("div", class_="value")
        if not safety_index:
            print(f"Safety index not found for {city}")
            return None
        
        return {
            "safety_index": float(safety_index.text.strip())
        }
    except Exception as e:
        print(f"Error scraping safety data for {city}: {e}")
        return None

def scrape_safety():
    print("Scraping safety data...")

    data = {}
    for city in cities:
        result = get_safety_data(city)
        if result:
            data[city] = result

    save_json(data, "../data/safety_data.json")
    print("Data saved to ../data/safety_data.json")

if __name__ == "__main__":
    scrape_safety()

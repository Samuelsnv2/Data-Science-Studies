import requests
from bs4 import BeautifulSoup
import json
from save_utils import save_json

cities = [
    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
    "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre",
    "Belém", "Goiânia", "Florianópolis", "Natal", "Vitória", "Santos"
]

# URL de exemplo (ajustar conforme o site desejado)
URL_TEMPLATE = "https://www.numbeo.com/transportation/in/{}/"

def get_transportation_data(city):
    try:
        city_formatted = city.lower().replace(" ", "-")
        url = URL_TEMPLATE.format(city_formatted)
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve data for {city}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Aqui você vai ajustar conforme a estrutura da página
        transportation_index = soup.find("div", class_="value")
        if not transportation_index:
            print(f"Transportation index not found for {city}")
            return None
        
        return {
            "transportation_index": float(transportation_index.text.strip())
        }
    except Exception as e:
        print(f"Error scraping transportation data for {city}: {e}")
        return None

def scrape_transportation():
    print("Scraping transportation data...")

    data = {}
    for city in cities:
        result = get_transportation_data(city)
        if result:
            data[city] = result

    save_json(data, "../data/transportation_data.json")
    print("Data saved to ../data/transportation_data.json")

if __name__ == "__main__":
    scrape_transportation()

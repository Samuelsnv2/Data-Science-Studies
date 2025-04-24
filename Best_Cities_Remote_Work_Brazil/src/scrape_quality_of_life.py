import requests
from bs4 import BeautifulSoup
import json
from save_utils import save_json

cities = [
    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
    "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre",
    "Belém", "Goiânia", "Florianópolis", "Natal", "Vitória", "Santos"
]

# URL de exemplo (pode ser ajustada para um site específico de qualidade de vida)
URL_TEMPLATE = "https://www.numbeo.com/quality-of-life/in/{}/"

def get_quality_of_life_data(city):
    try:
        city_formatted = city.lower().replace(" ", "-")
        url = URL_TEMPLATE.format(city_formatted)
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve data for {city}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Aqui você vai ajustar conforme a estrutura da página
        # Exemplo: procurar uma classe com dados de qualidade de vida
        quality_score = soup.find("div", class_="value")
        if not quality_score:
            print(f"Quality score not found for {city}")
            return None
        
        return {
            "quality_of_life_score": float(quality_score.text.strip())
        }
    except Exception as e:
        print(f"Error scraping quality of life for {city}: {e}")
        return None

def scrape_quality_of_life():
    print("Scraping quality of life data...")

    data = {}
    for city in cities:
        result = get_quality_of_life_data(city)
        if result:
            data[city] = result

    save_json(data, "../data/quality_of_life.json")
    print("Data saved to ../data/quality_of_life.json")

if __name__ == "__main__":
    scrape_quality_of_life()

import requests
from bs4 import BeautifulSoup
import json
from save_utils import save_json

cities = [
    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
    "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre",
    "Belém", "Goiânia", "Florianópolis", "Natal", "Vitória", "Santos"
]

def format_city_for_url(city):
    city = city.replace(" ", "-")
    if city == "Vitória":
        return "Vitoria"
    return city

def get_cost_of_living(city):
    try:
        formatted_city = format_city_for_url(city)
        url = f"https://www.numbeo.com/cost-of-living/in/{formatted_city}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Tenta encontrar o texto com a estimativa de custo mensal
        summary = soup.find("div", {"class": "seeding-call"}).text
        estimate_text = next(
            line for line in summary.split(".") if "Estimated monthly costs" in line
        )

        estimate = float(
            estimate_text.split("Estimated monthly costs")[1]
            .split("R$")[1]
            .split()[0]
            .replace(",", "")
        )

        return {"monthly_cost_single_person_brl": estimate}
    except Exception as e:
        print(f"Error scraping {city}: {e}")
        return None

def scrape_cost_of_living():
    print("Scraping cost of living data...")
    cost_data = {}

    for city in cities:
        data = get_cost_of_living(city)
        if data:
            cost_data[city] = data

    save_json(cost_data, "../data/cost_of_living.json")
    print("Data saved to ../data/cost_of_living.json")

if __name__ == "__main__":
    scrape_cost_of_living()

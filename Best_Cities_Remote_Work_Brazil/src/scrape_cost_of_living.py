import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class ExpatistanScraper:
    def __init__(self):
        self.base_url = "https://www.expatistan.com/cost-of-living"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.results_dir = "../data"
        os.makedirs(self.results_dir, exist_ok=True)

    def _save_data(self, data, filename):
        """Save data to a JSON file with timestamp."""
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"data": data, "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filepath}")

    def scrape_single_person_monthly_costs(self, city):
        """
        Scrape "Single person estimated monthly costs" for a specific city from Expatistan.
        """
        # Construct the URL for the city
        city_url = f"{self.base_url}/{city.lower().replace(' ', '-')}"
        try:
            # Fetch the webpage content
            response = requests.get(city_url, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find the section containing the single person estimated monthly costs
            cost_section = soup.find("div", class_="single-person-costs")
            if not cost_section:
                print(f"No 'Single person estimated monthly costs' found for {city}.")
                return None
            
            # Extract the cost value
            cost_value = cost_section.get_text(strip=True).replace("R$", "").replace(",", ".").strip()
            
            # Convert to float if possible
            try:
                cost_value = float(cost_value)
            except ValueError:
                print(f"Failed to parse cost value for {city}: {cost_value}")
                return None
            
            # Return the data as a dictionary
            return {"city": city, "single_person_monthly_costs": cost_value}
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {e}")
            return None

    def run_scraper(self, cities):
        """Run the scraper for the specified list of cities."""
        all_data = {}
        for city in cities:
            print(f"Scraping 'Single person estimated monthly costs' for {city}...")
            city_data = self.scrape_single_person_monthly_costs(city)
            if city_data:
                all_data[city] = city_data
                self._save_data(city_data, f"single_person_monthly_costs_{city.lower().replace(' ', '_')}.json")
            else:
                print(f"Failed to scrape data for {city}.")
        
        # Save all data to a consolidated JSON file
        self._save_data(all_data, "consolidated_single_person_monthly_costs.json")
        print("All data scraping complete!")

# Example usage
if __name__ == "__main__":
    scraper = ExpatistanScraper()
    brazilian_cities = [
        "Belo Horizonte", "Rio de Janeiro", "São Paulo", "Brasília", "Salvador",
        "Fortaleza", "Manaus", "Curitiba", "Recife", "Porto Alegre", "Belém",
        "Goiânia", "Florianópolis", "Natal", "Vitória", "Aracaju", "Palmas"
    ]
    scraper.run_scraper(brazilian_cities)
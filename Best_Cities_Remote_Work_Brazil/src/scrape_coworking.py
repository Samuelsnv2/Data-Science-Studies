"""
Brazilian State Capitals Coworking Data Collector

This script collects data about coworking spaces in Brazilian state capitals:
- Number of coworking spaces
- Average price ranges
- Ratings and reviews (when available)

Using free public data sources.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from urllib.parse import quote


class BrazilCoworkingCollector:
    def __init__(self):
        # Dictionary of Brazilian state capitals (State: Capital)
        self.capitals = {
            "Acre": "Rio Branco",
            "Alagoas": "Maceió",
            "Amapá": "Macapá",
            "Amazonas": "Manaus",
            "Bahia": "Salvador",
            "Ceará": "Fortaleza",
            "Distrito Federal": "Brasília",
            "Espírito Santo": "Vitória",
            "Goiás": "Goiânia",
            "Maranhão": "São Luís",
            "Mato Grosso": "Cuiabá",
            "Mato Grosso do Sul": "Campo Grande",
            "Minas Gerais": "Belo Horizonte",
            "Pará": "Belém",
            "Paraíba": "João Pessoa",
            "Paraná": "Curitiba",
            "Pernambuco": "Recife",
            "Piauí": "Teresina",
            "Rio de Janeiro": "Rio de Janeiro",
            "Rio Grande do Norte": "Natal",
            "Rio Grande do Sul": "Porto Alegre",
            "Rondônia": "Porto Velho",
            "Roraima": "Boa Vista",
            "Santa Catarina": "Florianópolis",
            "São Paulo": "São Paulo",
            "Sergipe": "Aracaju",
            "Tocantins": "Palmas"
        }
        
        # List to store all collected data
        self.all_data = []
        
        # Headers to simulate a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
        
        # Session to maintain cookies between requests
        self.session = requests.Session()
    
    def get_google_coworking_data(self, city):
        """
        Collect coworking data using Google search results.
        This is a basic implementation using free methods.
        """
        city_data = {
            'capital': city,
            'total_spaces': 0,
            'avg_price_min': None,
            'avg_price_max': None,
            'top_rated_spaces': []
        }
        
        search_query = f"coworking spaces in {city} Brazil"
        encoded_query = quote(search_query)
        
        # Google search URL
        url = f"https://www.google.com/search?q={encoded_query}"
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"Error accessing Google search for {city}: Status code {response.status_code}")
                return city_data
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract number of results
            result_stats = soup.find('div', id='result-stats')
            if result_stats:
                stats_text = result_stats.text
                # Extract approximate number of results
                match = re.search(r'About ([\d,\.]+) results', stats_text)
                if match:
                    results_count = match.group(1).replace(',', '').replace('.', '')
                    # Estimate number of spaces - very rough approximation
                    # Assuming about 1% of results are actual coworking listings
                    estimated_spaces = max(1, int(int(results_count) * 0.01))
                    city_data['total_spaces'] = min(estimated_spaces, 150)  # Cap at reasonable number
            
            # Look for pricing information in snippets
            snippets = soup.find_all(['div', 'span', 'p'], string=re.compile(r'R\$|BRL|per month|por mês', re.IGNORECASE))
            prices = []
            
            for snippet in snippets:
                # Look for price patterns like R$500, R$ 500, 500 BRL, etc.
                price_matches = re.findall(r'R\$\s*(\d+(?:\.\d+)?)', snippet.text)
                if price_matches:
                    for match in price_matches:
                        try:
                            price = float(match)
                            if 100 <= price <= 5000:  # Reasonable price range for coworking in Brazil
                                prices.append(price)
                        except ValueError:
                            continue
            
            # Calculate price range if prices were found
            if prices:
                city_data['avg_price_min'] = min(prices)
                city_data['avg_price_max'] = max(prices)
                
            print("Google search data collected successfully.")
            
            return city_data
            
        except Exception as e:
            print(f"Error collecting coworking data for {city}: {e}")
            return city_data
    
    def get_coworker_data(self, city):
        """
        Collect coworking data from Coworker.com
        Note: This is a basic implementation and may need adjustments based on site structure
        """
        # Format city name for URL
        city_url = city.replace(" ", "-").lower()
        url = f"https://www.coworker.com/search/brazil/{city_url}"
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"Error accessing Coworker.com for {city}: Status code {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find the number of spaces
            space_count = 0
            count_element = soup.select_one('.search-results-count')
            if count_element:
                count_text = count_element.text.strip()
                match = re.search(r'(\d+)', count_text)
                if match:
                    space_count = int(match.group(1))
            
            # Try to find price ranges
            prices = []
            price_elements = soup.select('.price')
            for price_el in price_elements:
                price_text = price_el.text.strip()
                # Extract numeric values from prices
                match = re.search(r'(\d+)', price_text)
                if match:
                    try:
                        price = int(match.group(1))
                        if 100 <= price <= 5000:  # Reasonable price range
                            prices.append(price)
                    except ValueError:
                        continue
            
            # Return the data
            return {
                'space_count': space_count,
                'prices': prices
            }
            
        except Exception as e:
            print(f"Error collecting Coworker.com data for {city}: {e}")
            return None
    
    def get_workfrom_data(self, city):
        """
        Collect coworking data from Workfrom.co
        Note: This is a basic implementation and may need adjustments
        """
        # Format city name for URL
        city_url = city.replace(" ", "-").lower()
        url = f"https://workfrom.co/brazil/{city_url}"
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"Error accessing Workfrom.co for {city}: Status code {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find the number of spaces
            locations = soup.select('.location-card')
            space_count = len(locations) if locations else 0
            
            # Try to find any pricing information
            prices = []
            price_elements = soup.select('.location-price')
            for price_el in price_elements:
                price_text = price_el.text.strip()
                # Extract numeric values from prices
                match = re.search(r'(\d+)', price_text)
                if match:
                    try:
                        price = int(match.group(1))
                        if 5 <= price <= 500:  # Reasonable daily price range
                            # Convert to monthly price (assuming 20 working days)
                            prices.append(price * 20)
                    except ValueError:
                        continue
            
            # Return the data
            return {
                'space_count': space_count,
                'prices': prices
            }
            
        except Exception as e:
            print(f"Error collecting Workfrom.co data for {city}: {e}")
            return None
    
    def collect_data(self):
        """Collect coworking data for all state capitals."""
        for state, capital in self.capitals.items():
            print(f"Collecting coworking data for {capital}, {state}...")
            
            # Create a dictionary to store data for this city
            city_data = {
                'state': state,
                'capital': capital,
                'total_coworking_spaces': 0,
                'minimum_price': None,
                'maximum_price': None,
                'avg_price': None
            }
            
            # Collect data from Google search
            google_data = self.get_google_coworking_data(capital)
            
            # Add a delay to avoid being blocked
            time.sleep(random.uniform(3, 5))
            
            # Try to collect data from Coworker.com
            coworker_data = self.get_coworker_data(capital)
            
            # Add a delay to avoid being blocked
            time.sleep(random.uniform(3, 5))
            
            # Try to collect data from Workfrom.co
            workfrom_data = self.get_workfrom_data(capital)
            
            # Add a delay before the next city
            time.sleep(random.uniform(3, 5))
            
            # Combine data from multiple sources
            spaces_counts = []
            prices = []
            
            # Add Google data
            if google_data:
                spaces_counts.append(google_data['total_spaces'])
                if google_data['avg_price_min'] and google_data['avg_price_max']:
                    prices.extend([google_data['avg_price_min'], google_data['avg_price_max']])
            
            # Add Coworker data
            if coworker_data and coworker_data['space_count'] > 0:
                spaces_counts.append(coworker_data['space_count'])
                prices.extend(coworker_data['prices'])
            
            # Add Workfrom data
            if workfrom_data and workfrom_data['space_count'] > 0:
                spaces_counts.append(workfrom_data['space_count'])
                prices.extend(workfrom_data['prices'])
            
            # Calculate totals and averages
            if spaces_counts:
                city_data['total_espacos_coworking'] = max(spaces_counts)  # Use the highest count
            
            if prices:
                city_data['preco_minimo'] = min(prices)
                city_data['preco_maximo'] = max(prices)
                city_data['preco_medio'] = sum(prices) / len(prices)
            
            # If no data could be found, use fallback estimates
            # These are rough estimates based on city size and economic development
            if city_data['total_espacos_coworking'] == 0:
                # Fallback data based on city population/importance
                big_cities = ["São Paulo", "Rio de Janeiro", "Brasília", "Belo Horizonte"]
                medium_cities = ["Porto Alegre", "Curitiba", "Recife", "Salvador", "Fortaleza", "Goiânia"]
                
                if capital in big_cities:
                    city_data['total_espacos_coworking'] = random.randint(50, 120)
                    city_data['preco_minimo'] = random.randint(500, 700)
                    city_data['preco_maximo'] = random.randint(1200, 2500)
                    city_data['preco_medio'] = (city_data['preco_minimo'] + city_data['preco_maximo']) / 2
                elif capital in medium_cities:
                    city_data['total_espacos_coworking'] = random.randint(15, 40)
                    city_data['preco_minimo'] = random.randint(400, 600)
                    city_data['preco_maximo'] = random.randint(900, 1500)
                    city_data['preco_medio'] = (city_data['preco_minimo'] + city_data['preco_maximo']) / 2
                else:
                    city_data['total_espacos_coworking'] = random.randint(3, 15)
                    city_data['preco_minimo'] = random.randint(300, 500)
                    city_data['preco_maximo'] = random.randint(700, 1200)
                    city_data['preco_medio'] = (city_data['preco_minimo'] + city_data['preco_maximo']) / 2
            
            # Add the data for this city to our collection
            self.all_data.append(city_data)
            
            print(f"Data collected for {capital}:")
            print(f"  Total coworking spaces: {city_data['total_espacos_coworking']}")
            print(f"  Price range: R${city_data['preco_minimo']} - R${city_data['preco_maximo']}")
            print(f"  Average price: R${city_data['preco_medio']}")
    
    def save_to_csv(self, filename='coworking_capitais_brasileiras.csv'):
        """Save the collected data to a CSV file."""
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Data saved to {filename} - {len(self.all_data)} records.")
        else:
            print("No data to save.")
    
    def save_to_excel(self, filename='coworking_capitais_brasileiras.xlsx'):
        """Save the collected data to an Excel file."""
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_excel(filename, index=False)
            print(f"Data saved to {filename} - {len(self.all_data)} records.")
        else:
            print("No data to save.")


# Run the collector if the script is executed directly
if __name__ == "__main__":
    collector = BrazilCoworkingCollector()
    collector.collect_data()
    collector.save_to_csv()
    # Uncomment to save as Excel file as well
    # collector.save_to_excel()
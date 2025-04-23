# Brazil Remote Work Cities - Web Scraping Tool
# This script collects data on various factors for analyzing the best cities for remote work in Brazil

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import random
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class BrazilRemoteWorkScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.cities = self._load_cities()
        self.results_dir = '../data'
        os.makedirs(self.results_dir, exist_ok=True)
        
    def _load_cities(self):
        # Top Brazilian cities by population (could be expanded)
        return [
            'São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 
            'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 
            'Recife', 'Porto Alegre', 'Belém', 'Goiânia', 'Florianópolis',
            'Natal', 'Vitória', 'Santos'
        ]
    
    def scrape_internet_quality(self):
        print("Scraping internet quality data...")
        chrome_driver_path = r"C:\Users\samue\OneDrive\Documents\chromedriver\chromedriver.exe"
        service = Service(chrome_driver_path)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get("https://www.speedtest.net/global-index")
            # Wait for the table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "index-table"))  # Adjust based on actual HTML
            )

            # Extract table rows
            table = driver.find_element(By.CLASS_NAME, "index-table")  # Adjust based on actual HTML structure
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row

            internet_data = {}
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                city = columns[0].text.strip()
                if city in self.cities:
                    internet_data[city] = {
                        'avg_download_mbps': float(columns[1].text.strip()),
                        'avg_upload_mbps': float(columns[2].text.strip()),
                        'fiber_availability': round(random.uniform(0.3, 0.9), 2),  # Placeholder
                        'isp_count': random.randint(3, 15)  # Placeholder
                    }
        except Exception as e:
            print(f"Error scraping internet quality data: {e}")
            return {}
        finally:
            driver.quit()

        # Save data
        self._save_data(internet_data, 'internet_quality.json')
        return internet_data
    
    def scrape_cost_of_living(self):
        print("Scraping cost of living data...")
        cost_data = {}
        base_url = "https://www.numbeo.com/cost-of-living/in/"

        for city in self.cities:
            url = f"{base_url}{city.replace(' ', '-')}"

            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                # Adjusted selectors to match Numbeo's structure
                rent_1br_center = soup.find('td', string='Apartment (1 bedroom) in City Centre').find_next('td').text
                utilities_monthly = soup.find('td', string='Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment').find_next('td').text
                internet_monthly = soup.find('td', string='Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)').find_next('td').text
                meal_inexpensive = soup.find('td', string='Meal, Inexpensive Restaurant').find_next('td').text
                public_transport = soup.find('td', string='One-way Ticket (Local Transport)').find_next('td').text
                cappuccino_price = soup.find('td', string='Cappuccino (regular)').find_next('td').text

                # Convert values to float after cleaning
                cost_data[city] = {
                    'monthly_rent_1br_center': float(rent_1br_center.replace(',', '').strip()),
                    'utilities_monthly': float(utilities_monthly.replace(',', '').strip()),
                    'internet_monthly': float(internet_monthly.replace(',', '').strip()),
                    'meal_inexpensive_restaurant': float(meal_inexpensive.replace(',', '').strip()),
                    'monthly_public_transport': float(public_transport.replace(',', '').strip()),
                    'cappuccino_price': float(cappuccino_price.replace(',', '').strip()),
                    'cost_index': round(random.uniform(30, 70), 1)  # Placeholder
                }
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue

        # Save data
        self._save_data(cost_data, 'cost_of_living.json')
        return cost_data
    
    def scrape_safety_data(self):
        print("Scraping safety data...")
        safety_data = {}
        base_url = "https://www.numbeo.com/crime/in/"

        for city in self.cities:
            url = f"{base_url}{city.replace(' ', '-')}"

            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                # Adjusted selectors to match Numbeo's structure
                safety_index = soup.find('td', string='Safety Index:').find_next('td').text
                crime_index = soup.find('td', string='Crime Index:').find_next('td').text

                safety_data[city] = {
                    'safety_index': float(safety_index.strip()),
                    'crime_index': float(crime_index.strip()),
                    'perceived_safety_day': round(random.uniform(40, 90), 1),  # Placeholder
                    'perceived_safety_night': round(random.uniform(20, 70), 1)  # Placeholder
                }
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue

        # Save data
        self._save_data(safety_data, 'safety_data.json')
        return safety_data
    
    def scrape_climate_data(self):
        print("Scraping climate data...")
        climate_data = {}
        api_key = "your_openweathermap_api_key_here"

        for city in self.cities:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            try:
                # Validate API response structure
                if 'main' in data:
                    temp = data['main']['temp']
                    humidity = data['main']['humidity']
                    climate_data[city] = {
                        'avg_annual_temp': temp,
                        'avg_annual_rainfall': random.randint(700, 2200),  # Placeholder
                        'rainy_days_per_year': random.randint(80, 160),  # Placeholder
                        'humidity_avg': humidity,
                        'sunshine_hours_annual': random.randint(1500, 3000),  # Placeholder
                        'comfort_index': round(random.uniform(40, 85), 1)  # Placeholder
                    }
                else:
                    print(f"Error scraping {city}: Missing 'main' key in API response.")
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue

        # Save data
        self._save_data(climate_data, 'climate_data.json')
        return climate_data
    
    def scrape_coworking_data(self):
        print("Scraping coworking data...")
        coworking_data = {}
        api_key = "your_google_maps_api_key_here"

        for city in self.cities:
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=coworking+in+{city}&key={api_key}"
            response = requests.get(url)
            data = response.json()

            try:
                spaces = []
                for result in data['results'][:5]:  # Limit to 5 spaces
                    spaces.append({
                        'name': result['name'],
                        'monthly_price': random.randint(300, 1200),  # Placeholder
                        'rating': result.get('rating', None),
                        'has_meeting_rooms': random.choice([True, False]),
                        'has_high_speed_internet': random.choice([True, True, True, False]),
                        'has_24_7_access': random.choice([True, False])
                    })

                coworking_data[city] = {
                    'total_spaces': len(data['results']),
                    'avg_monthly_price': random.randint(350, 1000),  # Placeholder
                    'spaces_per_100k_pop': round(random.uniform(1, 10), 1),  # Placeholder
                    'sample_spaces': spaces
                }
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue

        # Save data
        self._save_data(coworking_data, 'coworking_data.json')
        return coworking_data
    
    def scrape_transportation_data(self):
        print("Scraping transportation data...")
        transport_data = {}
        base_url = "https://moovit.com/city/"  # Example URL

        for city in self.cities:
            url = f"{base_url}{city.replace(' ', '-')}"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                public_transit_score = float(soup.find('div', {'class': 'transit-score'}).text.strip())
                walkability_score = float(soup.find('div', {'class': 'walkability-score'}).text.strip())
                bike_friendly_score = float(soup.find('div', {'class': 'bike-score'}).text.strip())

                transport_data[city] = {
                    'has_metro': random.choice([True, False]),  # Placeholder
                    'has_brt': random.choice([True, False]),  # Placeholder
                    'public_transit_score': public_transit_score,
                    'walkability_score': walkability_score,
                    'bicycle_friendly_score': bike_friendly_score,
                    'uber_availability': random.choice(['High', 'Medium', 'Low']),  # Placeholder
                    'avg_commute_time': random.randint(25, 70),  # Placeholder
                    'international_airport_distance': random.randint(0, 100)  # Placeholder
                }
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue

        # Save data
        self._save_data(transport_data, 'transportation_data.json')
        return transport_data
    
    def scrape_quality_of_life(self):
        print("Scraping quality of life data...")
        qol_data = {}
        base_url = "https://www.numbeo.com/quality-of-life/in/"

        for city in self.cities:
            url = f"{base_url}{city.replace(' ', '-')}"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                hdi = float(soup.find('td', string='HDI').find_next('td').text.strip())
                healthcare_quality = float(soup.find('td', string='Health Care').find_next('td').text.strip())
                education_quality = float(soup.find('td', string='Education').find_next('td').text.strip())

                qol_data[city] = {
                    'hdi': hdi,
                    'healthcare_quality': healthcare_quality,
                    'education_quality': education_quality,
                    'leisure_options_score': round(random.uniform(40, 95), 1),  # Placeholder
                    'cultural_offerings_score': round(random.uniform(40, 95), 1),  # Placeholder
                    'green_spaces_per_capita': round(random.uniform(5, 50), 1),  # Placeholder
                    'pollution_index': round(random.uniform(20, 80), 1),  # Placeholder
                    'overall_happiness_index': round(random.uniform(5, 9), 1)  # Placeholder
                }
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue

        # Save data
        self._save_data(qol_data, 'quality_of_life.json')
        return qol_data
    
    def _save_data(self, data, filename):
        """Save data to JSON file with timestamp"""
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Brazil Remote Work Cities Data Scraper'
            }, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filepath}")
    
    def compile_all_data(self):
        """Compile all collected data into a single consolidated dataset"""
        print("Compiling all data...")
        
        # Load all individual data files
        data_files = {
            'internet': os.path.join(self.results_dir, 'internet_quality.json'),
            'cost': os.path.join(self.results_dir, 'cost_of_living.json'),
            'safety': os.path.join(self.results_dir, 'safety_data.json'),
            'climate': os.path.join(self.results_dir, 'climate_data.json'),
            'coworking': os.path.join(self.results_dir, 'coworking_data.json'),
            'transport': os.path.join(self.results_dir, 'transportation_data.json'),
            'quality': os.path.join(self.results_dir, 'quality_of_life.json')
        }
        
        all_data = {}
        for category, filepath in data_files.items():
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    all_data[category] = loaded_data['data']
            else:
                print(f"Warning: {filepath} not found.")
        
        # Create consolidated dataset
        cities_data = []
        for city in self.cities:
            city_data = {'city': city}
            
            # Internet metrics
            if 'internet' in all_data and city in all_data['internet']:
                city_data['download_speed'] = all_data['internet'][city]['avg_download_mbps']
                city_data['upload_speed'] = all_data['internet'][city]['avg_upload_mbps']
                city_data['fiber_availability'] = all_data['internet'][city]['fiber_availability']
            
            # Cost metrics
            if 'cost' in all_data and city in all_data['cost']:
                city_data['rent_1br_center'] = all_data['cost'][city]['monthly_rent_1br_center']
                city_data['cost_index'] = all_data['cost'][city]['cost_index']
            
            # Safety metrics
            if 'safety' in all_data and city in all_data['safety']:
                city_data['safety_index'] = all_data['safety'][city]['safety_index']
                city_data['crime_index'] = all_data['safety'][city]['crime_index']
            
            # Climate metrics
            if 'climate' in all_data and city in all_data['climate']:
                city_data['avg_temp'] = all_data['climate'][city]['avg_annual_temp']
                city_data['comfort_index'] = all_data['climate'][city]['comfort_index']
            
            # Coworking metrics
            if 'coworking' in all_data and city in all_data['coworking']:
                city_data['coworking_spaces'] = all_data['coworking'][city]['total_spaces']
                city_data['avg_coworking_price'] = all_data['coworking'][city]['avg_monthly_price']
            
            # Transport metrics
            if 'transport' in all_data and city in all_data['transport']:
                city_data['public_transit_score'] = all_data['transport'][city]['public_transit_score']
                city_data['walkability'] = all_data['transport'][city]['walkability_score']
            
            # Quality of life metrics
            if 'quality' in all_data and city in all_data['quality']:
                city_data['hdi'] = all_data['quality'][city]['hdi']
                city_data['healthcare_score'] = all_data['quality'][city]['healthcare_quality']
            
            cities_data.append(city_data)
        
        # Create DataFrame and save as CSV
        df = pd.DataFrame(cities_data)
        csv_path = os.path.join(self.results_dir, 'brazil_remote_work_cities.csv')
        df.to_csv(csv_path, index=False)
        print(f"Consolidated data saved to {csv_path}")
        
        return df
    
    def run_all_scrapers(self):
        """Run all scraping functions and compile data"""
        print("Starting comprehensive data collection...")
        
        # Run all scrapers with delays to avoid overwhelming sources
        self.scrape_internet_quality()
        time.sleep(2)
        
        self.scrape_cost_of_living()
        time.sleep(2)
        
        self.scrape_safety_data()
        time.sleep(2)
        
        self.scrape_climate_data()
        time.sleep(2)
        
        self.scrape_coworking_data()
        time.sleep(2)
        
        self.scrape_transportation_data()
        time.sleep(2)
        
        self.scrape_quality_of_life()
        time.sleep(2)
        
        # Compile all data into a single dataset
        final_data = self.compile_all_data()
        
        print("All data collection complete!")
        return final_data


# Usage example
if __name__ == "__main__":
    scraper = BrazilRemoteWorkScraper()
    
    # Run all scrapers or run individual ones as needed
    # Example: only run internet and cost of living scrapers
    # scraper.scrape_internet_quality()
    # scraper.scrape_cost_of_living()
    
    # Or run all scrapers
    data = scraper.run_all_scrapers()
    
    # Display first few rows of final dataset
    print("\nSample of collected data:")
    print(data.head())
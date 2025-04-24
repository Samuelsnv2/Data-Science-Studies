import requests
import json
from datetime import datetime
import os

# OpenWeatherMap API key (replace with your actual API key)
API_KEY = "9962ce5547cbcf6761eb7639f4dddff1"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of Brazilian state capitals
brazil_state_capitals = [
    "Rio Branco", "Maceió", "Macapá", "Manaus", "Salvador", "Fortaleza",
    "Brasília", "Vitória", "Goiânia", "São Luís", "Cuiabá", "Campo Grande",
    "Belo Horizonte", "Belém", "João Pessoa", "Curitiba", "Recife", "Teresina",
    "Rio de Janeiro", "Natal", "Porto Alegre", "Porto Velho", "Boa Vista",
    "Florianópolis", "São Paulo", "Aracaju", "Palmas"
]

def fetch_climate_data(city):
    """Fetch climate data for a specific city using OpenWeatherMap API."""
    params = {
        "q": city + ",BR",  # City name with country code (Brazil = BR)
        "appid": API_KEY,
        "units": "metric"  # Use metric units (temperature in Celsius)
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        
        # Extract relevant climate data
        weather_data = {
            "city": city,
            "temperature_celsius": data["main"]["temp"],
            "humidity_percent": data["main"]["humidity"],
            "wind_speed_mps": data["wind"]["speed"],
            "weather_description": data["weather"][0]["description"],
            "timestamp": datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def save_data_to_json(data, filename):
    """Save the collected data to a JSON file."""
    filepath = os.path.join("/data", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Ensure the directory exists
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"data": data, "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filepath}")

def main():
    print("Fetching climate data for Brazilian state capitals...")
    
    climate_data = []
    for city in brazil_state_capitals:
        print(f"Fetching data for {city}...")
        city_data = fetch_climate_data(city)
        if city_data:
            climate_data.append(city_data)
    
    # Save the collected data to a JSON file
    save_data_to_json(climate_data, "climate_data.json")
    print("Climate data collection complete!")

if __name__ == "__main__":
    main()
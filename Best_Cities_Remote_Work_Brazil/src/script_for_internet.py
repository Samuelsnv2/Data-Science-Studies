# this is a script to extract the internet quality data from a HTML file and save it to a JSON file

import json
from bs4 import BeautifulSoup

file_path = "C:/Users/samue/OneDrive/Documents/Data-Science-Studies/Best_Cities_Remote_Work_Brazil/src/internet_data.txt"

# Load the raw HTML content from the file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all rows in the table
rows = soup.find_all("tr", class_="c3d0cf616 c-26ebb306")

# Prepare a list to store the extracted data
data = []

# Extract data from each row
for row in rows:
    # Extract city and state information
    city_info = row.find("a").text.strip()
    rank, city_state = city_info.split(" - ", 1)
    city, state = city_state.rsplit(" - ", 1)
    
    # Extract internet speed
    speed_text = row.find_all("td")[1].text.strip()
    speed = float(speed_text.replace(" Mbps", ""))
    
    # Append the extracted data to the list
    data.append({
        "rank": int(rank.strip("º")),  # Remove the degree symbol and convert to integer
        "city": city.strip(),
        "state": state.strip(),
        "speed_mbps": speed
    })

# Save the data to a JSON file
json_filename = "internet_quality.json"
with open(json_filename, mode="w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=2)

print(f"Data successfully saved to {json_filename}")
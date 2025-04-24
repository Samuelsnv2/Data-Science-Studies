import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Failed to fetch page: {e}")
        return None

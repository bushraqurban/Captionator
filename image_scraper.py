"""
This module is responsible for scraping image URLs from a given webpage.
It uses the `requests` library to fetch the webpage content
and `BeautifulSoup` to parse and extract image URLs.
"""

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def scrape_images_from_url(url):
    """
    Scrape image URLs from the given webpage URL.
    """
    try:
        response = requests.get(url, timeout=30)  # 30 seconds timeout
        response.raise_for_status()  # Raise an exception for HTTP error responses
        soup = BeautifulSoup(response.text, 'html.parser')
        img_elements = soup.find_all('img')
        img_urls = []

        for img in img_elements:
            img_url = img.get('src')
            if img_url:
                # Ensure proper URL format
                img_url = urljoin(url, img_url)
                if 'svg' not in img_url and '1x1' not in img_url:  # Filter out unwanted images
                    img_urls.append(img_url)

        return img_urls

    except requests.exceptions.RequestException as e:  # Catch network-related errors
        print(f"Request error: {e}")
    except Exception as e:  # Catch other unexpected exceptions
        print(f"Error while scraping images: {e}")
    return []
    
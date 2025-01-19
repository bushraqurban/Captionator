import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_images_from_url(url):
    """
    Scrape image URLs from the given webpage URL.
    """
    try:
        response = requests.get(url)
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

    except Exception as e:
        print(f"Error while scraping images: {e}")
        return []

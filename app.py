import requests
import streamlit as st
from image_scraper import scrape_images_from_url
from image_captioner import generate_caption
from file_handler import save_captions_to_csv

def generate_captions_from_url(url):
    """
    Orchestrates the scraping of images, caption generation, and saving to CSV.
    """
    img_urls = scrape_images_from_url(url)
    
    if not img_urls:
        return None
    
    captions = []
    for img_url in img_urls:
        try:
            # Attempt to generate caption for the image
            caption = generate_caption(img_url)
            captions.append([img_url, caption])
        except Exception as e:
            # Catch any exceptions that happen during caption generation
            st.warning(f"Error processing image {img_url}: {str(e)}")
    
    if captions:
        # Save captions to CSV and return the file path
        csv_file = save_captions_to_csv(captions)
        return csv_file
    else:
        return None

# Streamlit Interface
st.title("📸 **Captionator** ✏️")

st.markdown("""
Welcome to Captionator! This app scrapes images from the URL you provide and uses advanced AI to generate captions for each image.

## How it works:
- Paste any webpage URL that contains images (e.g., Wikipedia or blogs).
- Click the **Generate Captions** button to generate captions.
- After the captions are generated, download the captions file.
""")

# Input: URL of the webpage
url = st.text_input("Enter URL", placeholder="Paste a webpage URL")

# Button to generate captions
if st.button("Generate Captions"):
    if url:
        # Generate captions and get the CSV file
        file_path = generate_captions_from_url(url)
        
        if file_path:
            # If file is generated, provide download button
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download Captions CSV",
                    data=file,
                    file_name="captions.csv",
                    mime="text/csv"
                )
        else:
            st.error("No images or captions were generated. Please check the URL and ensure it contains images.")
    else:
        st.warning("Please enter a valid URL.")

import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr
import csv  # Import csv module for writing CSV

# Load the pretrained processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_captions_from_url(url):
    # Download the page
    response = requests.get(url)
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img elements
    img_elements = soup.find_all('img')
    captions = []
    
    # Iterate over each img element
    for img_element in img_elements:
        img_url = img_element.get('src')

        # Skip if the image is an SVG or too small (likely an icon)
        if 'svg' in img_url or '1x1' in img_url:
            continue

        # Correct the URL if it's malformed
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif not img_url.startswith('http://') and not img_url.startswith('https://'):
            continue  # Skip URLs that don't start with http:// or https://

        try:
            # Download the image
            response = requests.get(img_url)
            # Convert the image data to a PIL Image
            raw_image = Image.open(BytesIO(response.content))
            if raw_image.size[0] * raw_image.size[1] < 400:  # Skip very small images
                continue
            
            raw_image = raw_image.convert('RGB')

            # Process the image
            inputs = processor(raw_image, return_tensors="pt")
            # Generate a caption for the image
            out = model.generate(**inputs, max_new_tokens=50)
            # Decode the generated tokens to text
            caption = processor.decode(out[0], skip_special_tokens=True)

            # Add the caption to the list
            captions.append([img_url, caption])  # Store as a list of [img_url, caption]
        except Exception as e:
            captions.append([img_url, f"Error processing image {img_url}: {e}"])
            continue
    
    # If captions are generated, save them to a CSV file
    if captions:
        # Define the CSV file path
        csv_file = "captions.csv"
        
        # Write the captions to a CSV file
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(["Image URL", "Caption"])
            # Write each image URL and caption
            writer.writerows(captions)
        
        return csv_file  # Return the filename for download
    else:
        return "No captions generated."

# Create the Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("""
    # 📸 **Captionator** ✏️

    Welcome to Captionator! This app scrapes images from the URL you provide and uses advanced AI to generate captions for each image.

    ## How it works:
    - Paste any webpage URL that contains images (e.g., Wikipedia or blogs).
    - Click the **Generate Captions** button to generate captions.
    - After the captions are generated, download the captions file.
    """)
    
    # URL input box
    url_input = gr.Textbox(label="Enter URL", placeholder="Paste a webpage URL", lines=2)
    
    # Generate Captions button
    generate_button = gr.Button("Generate Captions")

    # Output for generated captions as a file
    caption_output = gr.File(label="Download Captions File")
    
    # Define the function that gets triggered when the user submits a URL
    def update_output(url):
        # Generate captions and save to a file
        file_path = generate_captions_from_url(url)
        return file_path

    # Trigger file generation and file download
    url_input.submit(update_output, inputs=url_input, outputs=caption_output)
    generate_button.click(update_output, inputs=url_input, outputs=caption_output)

# Launch the interface
iface.launch()

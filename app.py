import gradio as gr
from image_scraper import scrape_images_from_url
from image_captioner import generate_caption
from file_handler import save_captions_to_csv

def generate_captions_from_url(url):
    """
    Orchestrates the scraping of images, caption generation, and saving to CSV.
    """
    img_urls = scrape_images_from_url(url)
    captions = []

    for img_url in img_urls:
        caption = generate_caption(img_url)
        captions.append([img_url, caption])

    if captions:
        csv_file = save_captions_to_csv(captions)
        return csv_file
    else:
        return "No captions generated."

# Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("""
    # 📸 **Captionator** ✏️

    Welcome to Captionator! This app scrapes images from the URL you provide and uses advanced AI to generate captions for each image.

    ## How it works:
    - Paste any webpage URL that contains images (e.g., Wikipedia or blogs).
    - Click the **Generate Captions** button to generate captions.
    - After the captions are generated, download the captions file.
    """)

    url_input = gr.Textbox(label="Enter URL", placeholder="Paste a webpage URL", lines=2)
    generate_button = gr.Button("Generate Captions")
    caption_output = gr.File(label="Download Captions File")

    def update_output(url):
        file_path = generate_captions_from_url(url)
        return file_path

    url_input.submit(update_output, inputs=url_input, outputs=caption_output)
    generate_button.click(update_output, inputs=url_input, outputs=caption_output)

# Launch the interface
iface.launch()

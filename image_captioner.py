from io import BytesIO
from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize the BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_url):
    """
    Generate a caption for the given image URL using the BLIP model.
    """
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        if image.size[0] * image.size[1] < 400:  # Skip small images
            return None

        image = image.convert('RGB')  # Ensure the image is in RGB format

        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(out[0], skip_special_tokens=True)

        return caption

    except Exception as e:
        print(f"Error processing image {image_url}: {e}")
        return f"Error processing image {image_url}"

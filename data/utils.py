import requests
from PIL import Image
from io import BytesIO
import os

def get_image(url, save_dir,filename):
    """
    Input: Url, save_dir [NOT FULL XPATH]
    Returns: image_type
    downloads an image from a given URL, determines its file type, and saves it to a specified directory
    """
    try:
        # Send a request to fetch the image
        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image"):
            raise ValueError("The URL does not point to a valid image.")
        
        image = Image.open(BytesIO(response.content))

        # Get the image format
        image_type = image.format

        # If filename is not provided, derive it from the URL
        if not filename:
            filename = os.path.basename(url.split("?")[0])
        
        # Ensure the filename has the correct extension
        if not filename.lower().endswith(f".{image_type.lower()}"):
            filename += f".{image_type.lower()}"

        # Save the image
        file_path = os.path.join(save_dir, filename)
        image.save(file_path)

        return image_type, file_path

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download image: {e}")
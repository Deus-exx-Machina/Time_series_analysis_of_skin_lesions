import logging

import base64
from google import genai
from io import BytesIO
from PIL import Image

LOGGER = logging.getLogger(__name__)


class GeminiAPIHandler:
    def __init__(self, api_key, index, model_name="gemini-2.0-flash-exp"):
        """
        Initialize the Gemini API Client.

        Parameters:
        - api_key: str - Your Gemini API key.
        - model_name: str - The model to use (default: "gemini-2.0-flash-exp").
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.index = index
        self.model = model_name

    def generate_text(self, prompt):
        """
        Generate text content from a prompt.

        Parameters:
        - prompt: str - The text prompt to send to the model.

        Returns:
        - str - The generated text.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return None

    def generate_from_image_path(self, image_path, prompt):
        """
        Generate content based on an image and a text prompt.

        Parameters:
        - image_path (str): Path to the image file.
        - prompt (str): The text prompt to guide the generation.

        Returns:
        - str: The generated response text.
        """
        image = image.open(image_path)

        response = self.client.models.generate_content(
            model=self.model,
            contents=[image, prompt]
        )
        return response.text

    def generate_from_pil_image(self, pil_image, prompt):
        """
        Generate content based on a single PIL Image object and a text prompt.

        Parameters:
        - pil_image (PIL.Image.Image): A PIL Image object.
        - prompt (str): The text prompt to guide the generation.

        Returns:
        - str: The generated response text.
        """
        # Ensure the image is in RGB mode (convert from RGBA if necessary)
        if pil_image.mode == "RGBA":
            LOGGER.warning(
                "Image is in RGBA mode, converting to RGB for JPEG compatibility."
            )
            pil_image = pil_image.convert("RGB")
        elif pil_image.mode != "RGB":
            LOGGER.warning(
                f"Image is in {pil_image.mode} mode, converting to RGB for compatibility."
            )
            pil_image = pil_image.convert("RGB")

        # Keep the .jpeg format in memory and retrieve it as a byte string for faster processing
        with BytesIO() as img_buffer:
            pil_image.save(img_buffer, format="JPEG")
            image_bytes = img_buffer.getvalue()
        image = Image.open(BytesIO(image_bytes))
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[image, prompt]
        )
        return response.text


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f"../.env")

    gemini = GeminiAPIHandler(api_key=os.getenv("GEMINI_API_KEY"))

    text_prompt = "Do you know da wae?"
    print("Text Response:", gemini.generate_text(text_prompt))

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key and CSE ID from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')

class ImagenAI:
    def __init__(self, api_key, model="imagen-3.0-generate-002"):
        self.model = model
        self.api_key = api_key

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate_image(self, prompt, config=None):

        if config==None:
            config = config=types.GenerateImagesConfig(number_of_images= 1)

        response = self.client.models.generate_images(
            model=self.model,
            prompt=prompt,
            config=config
        )

        return response
    
if __name__ == "__main__":

    gemini_img = ImagenAI(api_key=google_api_key)
    
    prompt = """
    Create a table image based on below markdown:

    Table:

    | Column 1 | Column 2 |
    |---|---|
    | Row 1 Data | Row 1 Data |
    | Row 2 Data | Row 2 Data |
    
    """

    response = gemini_img.generate_image(prompt)

    for generated_image in response.generated_images:
        image = Image.open(BytesIO(generated_image.image.image_bytes))
        image.show()
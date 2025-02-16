from PIL import Image, ImageDraw, ImageFont
import textwrap


class ImageGenerator:

    def __init__(self):
        pass
    
    def convert_image_to_pil(self, image_path):

        # Load the image (supports both WEBP and PNG)
        image_path = image_path  # Replace with "image.png" for PNG images
        pil_image = Image.open(image_path)

        # Convert to RGB (if needed)
        pil_image = pil_image.convert("RGB")

        return pil_image

    def create_slide_with_image(self, heading, image_element, bullet_list):
         # Image dimensions (Full HD, 16:10 aspect ratio)
        width, height = 1920, 1200

        # Create a blank white image
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Define heading box properties
        heading_height = int(height * 0.12)  # 12% of image height
        heading_color = "darkblue"

        # Draw heading box
        draw.rectangle([0, 0, width, heading_height], fill=heading_color)

        # Load a font
        try:
            font = ImageFont.truetype("fonts/freesans-font/FreeSans-LrmZ.ttf", 65)
        except:
            font = ImageFont.load_default()

        # Calculate heading position (centered in heading box)
        text_bbox = draw.textbbox((0, 0), heading, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (width - text_width) // 2
        text_y = (heading_height - text_height) // 2

        # Draw heading text
        draw.text((text_x, text_y), heading, fill="white", font=font)

        # Define image and text area dimensions
        image_max_width = 800  # Limit image width to 800px
        content_y_start = heading_height + 30  # Space below heading
        content_height = height - content_y_start - 20
        text_area_width = width - image_max_width - 40  # Remaining space for text

        # Resize image to fit within its section while maintaining aspect ratio
        image_element.thumbnail((image_max_width, content_height))

        # Compute image placement (left side)
        image_x = 20
        image_y = content_y_start + (content_height - image_element.height) // 2

        # Paste the resized image onto the canvas
        image.paste(image_element, (image_x, image_y))

        # Create bullet points image
        bullet_image = Image.new("RGB", (text_area_width, content_height), "white")
        bullet_draw = ImageDraw.Draw(bullet_image)

        # Load font for bullets
        try:
            bullet_font = ImageFont.truetype("arial.ttf", 40)
        except:
            bullet_font = ImageFont.load_default()

        # Define bullet text properties
        bullet_x = 50  # Left padding
        bullet_radius = 12
        max_text_width = text_area_width - 60  # Maximum width for wrapped text
        bullet_y = 30  # Start position inside the bullet area

        # Draw bullets with word wrapping
        for bullet in bullet_list:
            wrapped_lines = textwrap.wrap(bullet, width=50)  # Adjust width as needed

            # Draw bullet circle
            bullet_draw.ellipse((bullet_x, bullet_y + 15, bullet_x + bullet_radius, bullet_y + 15 + bullet_radius), fill="gray")

            # Draw wrapped text
            text_y = bullet_y  # Start drawing text from the first line
            for line in wrapped_lines:
                bullet_draw.text((bullet_x + 30, text_y), line, fill="gray", font=bullet_font)
                text_y += 50  # Move to next line

            bullet_y = text_y + 20  # Space between bullet points

            # Stop drawing if bullets exceed the available space
            if bullet_y + 50 > content_height:
                break

        # Paste bullet points next to the image
        bullet_x_final = image_max_width + 30
        # bullet_y_final = content_y_start
        bullet_y_final = content_y_start + 120
        image.paste(bullet_image, (bullet_x_final, bullet_y_final))

        return image


    
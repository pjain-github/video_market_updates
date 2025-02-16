from video.video import create_video_with_audio_saved
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import datetime

def first_image(date=None):

    if date==None:
        today = datetime.date.today()
        formatted_date = today.strftime("%d %B %Y")
        date = str(formatted_date)


    # Image dimensions (Full HD)
    width = 1920
    height = 1080

    # Load the AI and candlestick chart image as the background
    ai_chart_path = "elements/first_page.jpg"  # **Important: Put the correct path here**
    try:
        img = Image.open(ai_chart_path)
        img = img.resize((width, height))  # Resize to Full HD dimensions
        draw = ImageDraw.Draw(img)

    except FileNotFoundError:
        print(f"AI chart image not found: {ai_chart_path}")
        img = Image.new("RGB", (width, height), (0, 0, 50))  # Blue background if not found
        draw = ImageDraw.Draw(img)
    except Exception as e:
        print(f"Error loading AI chart image: {e}")
        img = Image.new("RGB", (width, height), (0, 0, 50))  # Blue background if not found
        draw = ImageDraw.Draw(img)


    # YouTube logo (download and resize)
    yt_logo_url = "https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png"
    try:
        yt_logo_response = requests.get(yt_logo_url, stream=True)
        yt_logo_response.raise_for_status()

        content_type = yt_logo_response.headers.get('Content-Type')
        if not content_type or not content_type.startswith('image/'):
           raise ValueError(f"Invalid content type: {content_type}. Expected image/")

        yt_logo = Image.open(BytesIO(yt_logo_response.content)).convert("RGBA")
        yt_logo = yt_logo.resize((150, 100))

        logo_x = 20
        logo_y = 20
        img.paste(yt_logo, (logo_x, logo_y), yt_logo)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading YouTube logo: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e: # Catch any other image related error
        print(f"Error processing image: {e}")


    # Channel name
    font_path = "fonts/freesans-font/FreeSans-LrmZ.ttf"# Replace with the path to a font file
    try:
        font = ImageFont.truetype(font_path, size=50)
    except IOError:
        print(f"Font file not found: {font_path}")
        font = ImageFont.load_default()

    channel_name = "Fin Insights AI"
    channel_x = logo_x + yt_logo.width + 20
    channel_y = logo_y + (yt_logo.height // 2) - 25
    draw.text((channel_x, channel_y), channel_name, fill=(255, 255, 255), font=font)


    # Heading (Daily Market Updates) - At the bottom 3/4 of the page
    font_path_bold = "fonts/freesans-font/FreeSans-LrmZ.ttf"  # Try to find a bold Arial font (arialbd.ttf or similar)
    if not font_path_bold:
        font_path_bold = "fonts/freesans-font/FreeSans-LrmZ.ttf" # if bold font is not found then use normal font
    try:
        large_font = ImageFont.truetype(font_path_bold, size=50)  # Adjust size as needed
    except IOError:
        print(f"Bold Font file not found: {font_path_bold}")
        try:
            large_font = ImageFont.truetype(font_path, size=50) # use normal font
        except IOError:
            print(f"Font file not found: {font_path}")
            large_font = ImageFont.load_default()


    heading = f"Daily Market Updates by AI - {date}"

    # Use draw.textbbox() to get text size (or upgrade Pillow for draw.textsize())
    bbox = draw.textbbox((0, 0), heading, font=large_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    heading_x = (width - text_width) // 2  # Center horizontally
    heading_y = int(height * 0.75) - text_height // 2  # Bottom 3/4
    # or
    # heading_y = height - text_height - 20 # fixed space from bottom

    draw.text((heading_x, heading_y), heading, fill=(255, 255, 255), font=large_font)

    return img


class FirstPage:

    def __init__(self):
        pass

    @staticmethod
    def first_page():

        audio = "elements/intro_audio.wav"
        image = first_image()

        video = create_video_with_audio_saved(audio_path=audio, image=image)

        return video

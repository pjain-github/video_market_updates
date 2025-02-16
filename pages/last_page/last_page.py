from PIL import Image, ImageDraw, ImageFont
from video.video import create_video_with_audio_saved

def generate_end_screen(width=1920, height=1080):
    """Generates a blue-themed end screen image."""

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Blue Gradient Background
    color1 = (25, 118, 210)  # A nice blue
    color2 = (173, 216, 230)  # Light blue

    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line((0, y, width, y), fill=(r, g, b))

    font_size_thanks = 72  # Suggested size
    font_size_subscribe = 48  # Suggested size

    try:
        font_path = "fonts/freesans-font/FreeSansBold-Xgdd.ttf"  # ***REPLACE with actual path***
        font_thanks = ImageFont.truetype(font_path, font_size_thanks)
        font_subscribe = ImageFont.truetype(font_path, font_size_subscribe)
    except IOError:
        print("Font not found. Using default font.")
        font_thanks = ImageFont.load_default()
        font_subscribe = ImageFont.load_default()
        font_size_thanks = 40  # Smaller default size
        font_size_subscribe = 24  # Smaller default size

    text_thanks = "Thank You For Watching!"
    text_subscribe = "Subscribe for More Such Updates"

    thanks_bbox = draw.textbbox((0, 0), text_thanks, font=font_thanks)
    thanks_width = thanks_bbox[2] - thanks_bbox[0]
    thanks_height = thanks_bbox[3] - thanks_bbox[1]
    thanks_x = (width - thanks_width) / 2
    thanks_y = (height / 2) - thanks_height / 2 - 20

    subscribe_bbox = draw.textbbox((0, 0), text_subscribe, font=font_subscribe)
    subscribe_width = subscribe_bbox[2] - subscribe_bbox[0]
    subscribe_height = subscribe_bbox[3] - subscribe_bbox[1]
    subscribe_x = (width - subscribe_width) / 2
    subscribe_y = (height / 2) + subscribe_height / 2 + 20

    shadow_offset = 5
    draw.text((thanks_x + shadow_offset, thanks_y + shadow_offset), text_thanks, font=font_thanks, fill=(255, 255, 255))
    draw.text((subscribe_x + shadow_offset, subscribe_y + shadow_offset), text_subscribe, font=font_subscribe, fill=(255, 255, 255))

    text_color = (30, 30, 30)  # Dark gray/almost black
    draw.text((thanks_x, thanks_y), text_thanks, font=font_thanks, fill=text_color)
    draw.text((subscribe_x, subscribe_y), text_subscribe, font=font_subscribe, fill=text_color)

    return img

class LastPage:

    def __init__(self):
        pass

    @staticmethod
    def last_page():

        audio = "elements/outro_audio.wav"
        image = generate_end_screen()

        video = create_video_with_audio_saved(audio_path=audio, image=image)

        return video
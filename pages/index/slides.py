from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import textwrap
import io


class ImageGenerator:

    def __init__(self):
        pass

    def matplotlib_to_pil(self, fig):
        """Convert a Matplotlib figure to a PIL image."""
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        buf = np.asarray(canvas.buffer_rgba())
        return Image.fromarray(buf)

    def index_df_to_image(self, df):
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.set_axis_off()

        table = ax.table(cellText=df.values,  
                         colLabels=df.columns,  
                         cellLoc='center', 
                         loc='center',
                         colColours=["#0A2A66"] * len(df.columns))  

        table.auto_set_font_size(False)
        table.set_fontsize(10)

        for key, cell in table.get_celld().items():
            row, col = key
            cell.set_edgecolor("#D3D3D3")  
            if row == 0:
                cell.set_text_props(color="white", weight="bold")  
            else:
                cell.set_text_props(color="grey")  

        # Save figure to a BytesIO buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
        plt.close(fig)  # Close the figure to free memory

        # Convert buffer to PIL Image
        buf.seek(0)
        image = Image.open(buf)

        return image
    
    def plot_candlestick_chart(self, df, months=3):
        # Convert Date column to datetime format
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

        # Filter data for the last specified months
        df = df.sort_values("Date")
        last_date = df["Date"].max()
        start_date = last_date - pd.DateOffset(months=months)
        filtered_data = df[df["Date"] >= start_date]

        # Set the index to Date for mplfinance
        filtered_data.set_index("Date", inplace=True)

        # Create a candlestick chart
        plt.figure(figsize=(8, 8))
        fig, ax = mpf.plot(filtered_data, type='candle', style='charles', volume=True, ylabel='Price', returnfig=True)

        # # Save figure to a BytesIO buffer
        # buf = io.BytesIO()
        # fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
        # plt.close(fig)  # Close the figure to free memory

        # # Convert buffer to PIL Image
        # buf.seek(0)
        # image = Image.open(buf)

        return fig
    
    
    def create_nifty_with_image(self, heading, image_element, right_top_image, bullet_list):
        # Image dimensions (Full HD, 16:10 aspect ratio)
        width, height = 1920, 1200

        # Create a blank white image
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Define heading box properties
        heading_height = int(height * 0.12)  # 12% of image height
        heading_color = "darkblue"
        draw.rectangle([0, 0, width, heading_height], fill=heading_color)

        # Load a font
        try:
            font = ImageFont.truetype("fonts/freesans-font/FreeSans-LrmZ.ttf", 65)
        except:
            font = ImageFont.load_default()

        # Calculate heading position (centered in heading box)
        text_bbox = draw.textbbox((0, 0), heading, font=font)
        text_x = (width - (text_bbox[2] - text_bbox[0])) // 2
        text_y = (heading_height - (text_bbox[3] - text_bbox[1])) // 2
        draw.text((text_x, text_y), heading, fill="white", font=font)

        # Define content dimensions
        content_y_start = heading_height + 20  # Start below heading
        content_height = height - content_y_start - 20  # Available height

        # Convert matplotlib figures to PIL images
        image_element = self.matplotlib_to_pil(image_element)
        # right_top_image = self.matplotlib_to_pil(right_top_image)

        # Resize left-side matplotlib image to 800x800
        image_element = image_element.resize((800, 800))
        image_x = 0  # Left padding
        image_y = content_y_start + (content_height - 800) // 2
        image.paste(image_element, (image_x, image_y))

        # Resize right-side upper image to 1000x300
        right_top_image = right_top_image.resize((900, 450))
        right_top_x = 900  # Fixed x position for right image
        right_top_y = content_y_start + 50
        image.paste(right_top_image, (right_top_x, right_top_y))

        # Define bullet points area dimensions
        right_bottom_height = content_height - 300  # Remaining space below right-top image

        # Create bullet points image
        bullet_image = Image.new("RGB", (1000, right_bottom_height), "white")
        bullet_draw = ImageDraw.Draw(bullet_image)

        # Load font for bullets
        try:
            bullet_font = ImageFont.truetype("arial.ttf", 40)
        except:
            bullet_font = ImageFont.load_default()

        # Define bullet text properties
        bullet_x = 50  # Left padding
        bullet_radius = 12
        max_text_width = 1000  # Maximum width for wrapped text
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
            if bullet_y + 50 > right_bottom_height:
                break

        # Paste bullet points below right-top image
        bullet_x_final = right_top_x - 50
        bullet_y_final = right_top_y + 325  # Right image height is 300
        image.paste(bullet_image, (bullet_x_final, bullet_y_final))

        return image
from PIL import Image, ImageDraw
from image import bullet_to_img, heading_to_img, table_to_img

bullet_path = 'elements/bullet_image.png'
table_path = 'elements/table_image.png'
header_path = 'elements/header_image.png'
output_path = 'elements/combined_image.png'

def combine_images(header_path, left_image_path, right_image_path, output_path):

    # Load images
    header = Image.open(header_path)  # 1600x100
    left_image = Image.open(left_image_path)  # 500x500
    right_image = Image.open(right_image_path)  # 1000x700

    # Define final image size
    final_width = 800
    final_height = 500
    padding = 25  # Padding between images
    border_width = 0  # Border thickness
    border_color = (255, 255, 255)  # WHITE border

    # Create a blank image with white background
    final_image = Image.new("RGB", (final_width, final_height), "white")

    # Add borders to images
    def add_border(img, border_width, border_color):
        bordered_img = Image.new("RGB", (img.width + 2 * border_width, img.height + 2 * border_width), border_color)
        bordered_img.paste(img, (border_width, border_width))
        return bordered_img

    # Apply borders
    header = add_border(header, border_width, border_color)
    left_image = add_border(left_image, border_width, border_color)
    right_image = add_border(right_image, border_width, border_color)

    # Paste images onto final image
    final_image.paste(header, (0, 0))

    left_x = padding
    left_y = header.height + padding + (final_height-header.height-left_image.height)//3
    final_image.paste(left_image, (left_x, left_y))

    right_x = 325
    right_y = header.height + padding
    final_image.paste(right_image, (right_x, right_y))

    # Save the final combined image
    final_image.save(output_path)
    return output_path
    # final_image.show()

def combine_images_without_bullet_points(header_path, left_image_path, output_path):

    # Load images
    header = Image.open(header_path)  # 1600x100
    left_image = Image.open(left_image_path)  # 500x500
    # Define final image size
    final_width = 800
    final_height = 500
    padding = 25  # Padding between images
    border_width = 0  # Border thickness
    border_color = (255, 255, 255)  # WHITE border

    # Create a blank image with white background
    final_image = Image.new("RGB", (final_width, final_height), "white")

    # Add borders to images
    def add_border(img, border_width, border_color):
        bordered_img = Image.new("RGB", (img.width + 2 * border_width, img.height + 2 * border_width), border_color)
        bordered_img.paste(img, (border_width, border_width))
        return bordered_img

    # Apply borders
    header = add_border(header, border_width, border_color)
    left_image = add_border(left_image, border_width, border_color)

    # Paste images onto final image
    final_image.paste(header, (0, 0))

    left_x = (final_width - left_image.width)//2
    left_y = header.height + padding + (final_height-header.height-left_image.height)//3
    final_image.paste(left_image, (left_x, left_y))

    # Save the final combined image
    final_image.save(output_path)
    return output_path
    # final_image.show()

def combine_images_without_tables(header_path, right_image_path, output_path):

    # Load images
    header = Image.open(header_path)  # 1600x100
    right_image = Image.open(right_image_path)  # 1000x700

    # Define final image size
    final_width = 800
    final_height = 500
    padding = 25  # Padding between images
    border_width = 0  # Border thickness
    border_color = (255, 255, 255)  # WHITE border

    # Create a blank image with white background
    final_image = Image.new("RGB", (final_width, final_height), "white")

    # Add borders to images
    def add_border(img, border_width, border_color):
        bordered_img = Image.new("RGB", (img.width + 2 * border_width, img.height + 2 * border_width), border_color)
        bordered_img.paste(img, (border_width, border_width))
        return bordered_img

    # Apply borders
    header = add_border(header, border_width, border_color)
    right_image = add_border(right_image, border_width, border_color)

    # Paste images onto final image
    final_image.paste(header, (0, 0))

    right_x = padding
    right_y = header.height + padding//5
    final_image.paste(right_image, (right_x, right_y))

    # Save the final combined image
    final_image.save(output_path)
    return output_path
    # final_image.show()

def generate_element_images(bullet_points, table_html, heading_text, output_path=output_path):
    # Generate images for each element
    html_bullets = bullet_to_img.generate_bullet_points_html(bullet_points)
    bullet_to_img.html_to_image_selenium(html_bullets, bullet_path)
    
    modified_html = table_to_img.modify_table_style(table_html)
    table_to_img.html_to_image_selenium(modified_html, table_path)
    
    html_string = heading_to_img.generate_html(heading_text)
    heading_to_img.html_to_image_selenium(html_string, header_path)
    
    return combine_images(header_path, table_path, bullet_path, output_path)

def generate_element_images_without_bullet_points(table_html, heading_text, output_path=output_path):
    # Generate images for each element
    modified_html = table_to_img.modify_table_style(table_html)
    table_to_img.html_to_image_selenium(modified_html, table_path)
    
    html_string = heading_to_img.generate_html(heading_text)
    heading_to_img.html_to_image_selenium(html_string, header_path)
    
    return combine_images_without_bullet_points(header_path, table_path, output_path)

def generate_element_images_without_table(bullet_points, heading_text, output_path=output_path):
    # Generate images for each element
    html_bullets = bullet_to_img.generate_bullet_points_without_image_html(bullet_points)
    bullet_to_img.html_to_image_selenium(html_bullets, bullet_path)
    
    html_string = heading_to_img.generate_html(heading_text)
    heading_to_img.html_to_image_selenium(html_string, header_path)
    
    return combine_images_without_tables(header_path, bullet_path, output_path)

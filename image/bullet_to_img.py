import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By


def generate_bullet_points_html(bullet_points):
    bullet_list = "".join(f'<li style="margin-bottom: 10px;">{point}</li>' for point in bullet_points)
    html_template = f'''
    <div style="
        width: 450px;
        height: 350px;
        background-color: white;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        color: grey;
        font-size: 22px;
        font-weight: bold;
        text-align: left;
        padding-top: 20px;
        padding-left: 20px;
    ">
        <ul style="list-style-type: disc; padding: 20px; text-align: left;">
            {bullet_list}
        </ul>
    </div>
    '''
    return html_template

def generate_bullet_points_without_image_html(bullet_points):
    bullet_list = "".join(f'<li style="margin-bottom: 10px;">{point}</li>' for point in bullet_points)
    html_template = f'''
    <div style="
        width: 750px;
        height: 350px;
        background-color: white;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        color: grey;
        font-size: 22px;
        font-weight: bold;
        text-align: left;
        padding-top: 10px;
        padding-left: 10px;
    ">
        <ul style="list-style-type: disc; padding: 20px; text-align: left;">
            {bullet_list}
        </ul>
    </div>
    '''
    return html_template

def html_to_image_selenium(html_string, output_filename="bullet_image.png"):
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html:
        temp_html.write(html_string.encode("utf-8"))
        temp_html_path = temp_html.name

    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--window-size=1000x1000")  # Adjust window size for capturing element
    driver = webdriver.Chrome(options=options)

    try:
        # Open the HTML file
        driver.get("file://" + temp_html_path)

        # Wait for the element to load
        time.sleep(2)  # Ensure element is fully loaded

        # Locate the div element and take a screenshot
        element = driver.find_element(By.TAG_NAME, "div")
        element.screenshot(output_filename)

        print(f"Element image saved to {output_filename}")
    finally:
        driver.quit()
        return output_filename

if __name__ == "__main__":
    bullet_points = ["Point 1", "Point 2", "Point 3", "Point 4"]
    bullet_html = generate_bullet_points_html(bullet_points)
    html_to_image_selenium(bullet_html, "bullet_image.png")
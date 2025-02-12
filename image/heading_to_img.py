import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By

def generate_html(text):
    html_template = f'''
    <div style="
        width: 800px;
        height: 65px;
        background-color: darkblue;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    ">
        {text}
    </div>
    '''
    return html_template

def html_to_image_selenium(html_string, output_filename="header_image.png"):
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html:
        temp_html.write(html_string.encode("utf-8"))
        temp_html_path = temp_html.name

    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--window-size=200x2000")  # Adjust window size for capturing element
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
    html_string = generate_html("New idea on how to generate image")
    html_to_image_selenium(html_string)

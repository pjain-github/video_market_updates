from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import tempfile

def generate_market_updates_html(custom_text):
    html_template = f'''
    <div style="
        width: 800px;
        height: 500px;
        background-color: #002366; /* Dark Blue */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        font-family: 'Arial', sans-serif;
    ">
        <div style="font-size: 50px; font-family: 'Cursive', sans-serif; margin-bottom: 20px;">
            Fin Insights AI
        </div>
        <div>
            {custom_text}
        </div>
    </div>
    '''
    return html_template


def generate_end_screen_html():
    html_template = '''
    <div style="
        width: 800px;
        height: 500px;
        background-color: #002366; /* Dark Blue */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        font-family: 'Arial', sans-serif;
    ">
        <div style="margin-bottom: 20px;">Thank you for watching!</div>
        <div>Subscribe to keep yourself updated</div>
    </div>
    '''
    return html_template

def html_to_image_selenium(html_string, output_filename="market_updates.png"):
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html:
        temp_html.write(html_string.encode("utf-8"))
        temp_html_path = temp_html.name

    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--window-size=1000x1000")  # Adjust window size
    driver = webdriver.Chrome(options=options)

    try:
        # Open the HTML file
        driver.get("file://" + temp_html_path)
        time.sleep(2)  # Ensure element is fully loaded

        # Locate the div element and take a screenshot
        element = driver.find_element(By.TAG_NAME, "div")
        element.screenshot(output_filename)

        print(f"Element image saved to {output_filename}")
    finally:
        driver.quit()
        return output_filename

if __name__ == "__main__":
    custom_text = "Daily Market Updates by AI"
    market_html = generate_market_updates_html(custom_text)
    html_to_image_selenium(market_html, "elements/market_updates.png")

    market_html = generate_end_screen_html()
    html_to_image_selenium(market_html, "elements/end_screen.png")
    

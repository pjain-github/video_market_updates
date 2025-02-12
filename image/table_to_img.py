import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
    

def modify_table_style(html_content):
    """
    Modifies HTML table styles to have dark blue header background,
    white header text, grey cell text, and a fixed size container.

    Args:
        html_content: The HTML content as a string.

    Returns:
        The modified HTML content as a string, or None if there's an error.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Create the container div
        container = soup.new_tag('div', id='table-container')

        # Find the table and wrap it in the container
        table = soup.find('table')
        if table:
            table.wrap(container)
        else:
            return None  # Return None if there's no table

        # Style the container
        container['style'] = "width: 275px; height: 350px; overflow: visible;"

        # Style the table
        table['style'] = "width: 100%; border-collapse: collapse;"

        # Style table headers
        for th in soup.find_all('th'):
            th['style'] = "background-color: darkblue; color: white; padding: 8px; text-align: left;"

        # Style table cells
        for td in soup.find_all('td'):
            td['style'] = "color: grey; padding: 8px; border-bottom: 1px solid #ddd;"

        # Add hover effect (optional)
        style_tag = soup.new_tag('style')
        style_tag.string = """
        tr:hover {
            background-color: #f2f2f2;
        }
        """

        # Ensure there's a head tag in the document
        if not soup.head:
            soup.insert(0, soup.new_tag("head"))

        soup.head.append(style_tag)  # Append the style tag to the head

        return str(soup)
    except Exception as e:
        print(f"An error occurred while generating table images: {e}")
        return None
    
def modify_only_table_style(html_content):
    """
    Modifies HTML table styles to have dark blue header background,
    white header text, grey cell text, and a fixed size container.

    Args:
        html_content: The HTML content as a string.

    Returns:
        The modified HTML content as a string, or None if there's an error.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Create the container div
        container = soup.new_tag('div', id='table-container')

        # Find the table and wrap it in the container
        table = soup.find('table')
        if table:
            table.wrap(container)
        else:
            return None  # Return None if there's no table

        # Style the container
        container['style'] = "width: 600px; height: 350px; overflow: visible;"

        # Style the table
        table['style'] = "width: 100%; border-collapse: collapse;"

        # Style table headers
        for th in soup.find_all('th'):
            th['style'] = "background-color: darkblue; color: white; padding: 8px; text-align: left;"

        # Style table cells
        for td in soup.find_all('td'):
            td['style'] = "color: grey; padding: 8px; border-bottom: 1px solid #ddd;"

        # Add hover effect (optional)
        style_tag = soup.new_tag('style')
        style_tag.string = """
        tr:hover {
            background-color: #f2f2f2;
        }
        """

        # Ensure there's a head tag in the document
        if not soup.head:
            soup.insert(0, soup.new_tag("head"))

        soup.head.append(style_tag)  # Append the style tag to the head

        return str(soup)
    except Exception as e:
        print(f"An error occurred while generating table images: {e}")
        return None

def html_to_image_selenium(html_string, output_filename="table_image.png"):
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html:
        temp_html.write(html_string.encode("utf-8"))
        temp_html_path = temp_html.name

    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--window-size=1000x1000")  # Adjust window size for capturing table
    driver = webdriver.Chrome(options=options)

    try:
        # Open the HTML file
        driver.get("file://" + temp_html_path)

        # Wait for the table to load
        time.sleep(2)  # Ensure table is fully loaded

        # Locate the table and take a screenshot
        table = driver.find_element(By.TAG_NAME, "table")
        table.screenshot(output_filename)

        print(f"Table image saved to {output_filename}")
    finally:
        driver.quit()
        return output_filename

if __name__=="__main__":

    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Example</title>
    </head>
    <body>
    <table>
      <thead>
        <tr>
          <th>Firstname</th>
          <th>Lastname</th>
          <th>Age</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Jill</td>
          <td>Smith</td>
          <td>50</td>
        </tr>
        <tr>
          <td>Eve</td>
          <td>Jackson</td>
          <td>94</td>
        </tr>
      </tbody>
    </table>
    </body>
    </html>
    """

    modified_html = modify_table_style(html_string)
    html_to_image_selenium(modified_html, "table_image.png") if modified_html else print("Error in modifying HTML")




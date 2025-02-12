import requests
from bs4 import BeautifulSoup
import logging
import threading
from functools import wraps

def timeout_handler(seconds=20):
    """Decorator to timeout a function if it exceeds the given time limit."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None, None]  # Default return if timeout occurs

            def target():
                try:
                    result[0], result[1] = func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error in function {func.__name__}: {e}")

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                logging.warning(f"Function {func.__name__} timed out after {seconds} seconds.")
                return None, None  # Timeout case
            
            return result[0], result[1]

        return wrapper
    return decorator



# Send a GET request to the URL
class WebScraper:
    """
    A class to scrape the title and text content of a webpage.
    Asynchronous and synchronous methods are provided for fetching the webpage content.
    """
    
    # @staticmethod
    # def get_article(url):
    #     """
    #     Sends a GET request to the given URL and retrieves the title and text content of the webpage.

    #     Parameters:
    #     - url (str): The URL of the webpage to scrape.

    #     Returns:
    #     - title (str): The title of the webpage.
    #     - text (str): The text content of the webpage.
    #     """
        
    #     try:
    #         logging.info(f"Fetching webpage content from {url}")
    #         response = requests.get(url, timeout=15)

    #         text = ''
    #         if response.status_code == 200:
    #             # Parse the HTML content of the webpage
    #             soup = BeautifulSoup(response.content, 'html.parser')
    
    #             # Getting title of the page
    #             title = soup.title.string if soup.title else "No title found"
    
    #             text = ''
    
    #             # Getting text from webpage            
    #             text_content = [p.get_text(strip=True) for p in soup.find_all('p')]
    #             for text_part in text_content:
    #                 text = text + text_part + '\n'

    #             logging.info(f"Webscrapping completed from {url}")

    #         else:
    #             print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    #             title = ''

    #     except Exception as e:
    #         print("Failed to get text")
    #         # Extract all the text from the webpage
    #         return None, None

    #     return title, text
    
    @staticmethod
    @timeout_handler(120)
    def get_article(url):

        def truncate_base64(content):
            """Truncate base64-encoded data to only keep till 'jpeg'"""
            if "base64" in content:
                parts = content.split("base64,")
                return parts[0] if len(parts) > 1 else content
            return content

        try:
            logging.info(f"Fetching webpage content from {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # List to store extracted content
            content_list = []

            # Iterate over all elements in the body
            for element in soup.body.descendants:
                if element.name == 'p':  # Paragraph text
                    content = element.get_text(strip=True)
                    if content:
                        content_list.append({'type': 'text', 'content': truncate_base64(content)})

                elif element.name == 'img':  # Images
                    img_src = element.get('src')
                    if img_src:
                        full_url = requests.compat.urljoin(url, img_src)
                        content_list.append({'type': 'image', 'content': truncate_base64(full_url)})

                elif element.name == 'table':  # Tables
                    table_html = str(element)
                    content_list.append({'type': 'table', 'content': truncate_base64(table_html)})

                elif element.name == 'a':  # Links
                    link_href = element.get('href')
                    link_text = element.get_text(strip=True)
                    if link_href:
                        full_url = requests.compat.urljoin(url, link_href)
                        content_list.append({'type': 'link', 'content': {'url': truncate_base64(full_url), 'text': truncate_base64(link_text)}})

            text = ""
            image_list = []

            # Stringify the extracted content
            for item in content_list:
                if item['type'] == 'text':
                    text += f"Text: {item['content']}\n"
                elif item['type'] == 'image':
                    image_list.append(item['content'])
                elif item['type'] == 'table':
                    text += f"Table HTML: {item['content']}\n"

            logging.info(f"Webscrapping completed from {url}")

            return text, image_list

        except:
            return None, None
    
    @staticmethod
    @timeout_handler(120)
    def extract_content_with_sequence(url):

        def truncate_base64(content):
            """Truncate base64-encoded data to only keep till 'jpeg'"""
            if "base64" in content:
                parts = content.split("base64,")
                return parts[0] if len(parts) > 1 else content
            return content

        try:
            logging.info(f"Fetching webpage content from {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # List to store extracted content
            content_list = []

            # Iterate over all elements in the body
            for element in soup.body.descendants:
                if element.name == 'p':  # Paragraph text
                    content = element.get_text(strip=True)
                    if content:
                        content_list.append({'type': 'text', 'content': truncate_base64(content)})

                elif element.name == 'img':  # Images
                    img_src = element.get('src')
                    if img_src:
                        full_url = requests.compat.urljoin(url, img_src)
                        content_list.append({'type': 'image', 'content': truncate_base64(full_url)})

                elif element.name == 'table':  # Tables
                    table_html = str(element)
                    content_list.append({'type': 'table', 'content': truncate_base64(table_html)})

                elif element.name == 'a':  # Links
                    link_href = element.get('href')
                    link_text = element.get_text(strip=True)
                    if link_href:
                        full_url = requests.compat.urljoin(url, link_href)
                        content_list.append({'type': 'link', 'content': {'url': truncate_base64(full_url), 'text': truncate_base64(link_text)}})

            text = ""
            image_list = []

            # Stringify the extracted content
            for item in content_list:
                if item['type'] == 'text':
                    text += f"Text: {item['content']}\n"
                elif item['type'] == 'image':
                    text += f"Image URL: {item['content']}\n"
                    image_list.append(item['content'])
                elif item['type'] == 'table':
                    text += f"Table HTML: {item['content']}\n"
                elif item['type'] == 'link':
                    text += f"Link: {item['content']['url']} (Text: {item['content']['text']})\n"

            logging.info(f"Webscrapping completed from {url}")

            return text, image_list

        except:
            return None, None

    # def extract_content_with_sequence(url):
    #     try:
    #         response = requests.get(url)
    #         soup = BeautifulSoup(response.content, 'html.parser')

    #         # List to store extracted content
    #         content_list = []

    #         # Iterate over all elements in the body
    #         for element in soup.body.descendants:
    #             if element.name == 'p':  # Paragraph text
    #                 content = element.get_text(strip=True)
    #                 if content:
    #                     content_list.append({'type': 'text', 'content': content})

    #             elif element.name == 'img':  # Images
    #                 img_src = element.get('src')
    #                 if img_src:
    #                     full_url = requests.compat.urljoin(url, img_src)
    #                     content_list.append({'type': 'image', 'content': full_url})

    #             elif element.name == 'table':  # Tables
    #                 table_html = str(element)
    #                 content_list.append({'type': 'table', 'content': table_html})

    #             elif element.name == 'a':  # Links
    #                 link_href = element.get('href')
    #                 link_text = element.get_text(strip=True)
    #                 if link_href:
    #                     full_url = requests.compat.urljoin(url, link_href)
    #                     content_list.append({'type': 'link', 'content': {'url': full_url, 'text': link_text}})

    #         text = ""

    #         # Stringigy the extracted content
    #         for item in content_list:
    #             if item['type'] == 'text':
    #                 text += f"Text: {item['content']}\n"
    #             elif item['type'] == 'image':
    #                  text += f"Image URL: {item['content']}\n"
    #             elif item['type'] == 'table':
    #                  text += f"Table HTML: {item['content']}\n"
    #             elif item['type'] == 'link':
    #                  text += f"Link: {item['content']['url']} (Text: {item['content']['text']})\n"
            
    #         return text
        
    #     except:
    #         return None

if __name__ == "__main__":
    url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"
    title, text = WebScraper.extract_content_with_sequence(url)
    print(f"Title: {title}")
    print(f"Text: {text}")
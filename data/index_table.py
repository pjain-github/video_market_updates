import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import logging
from data.web_scrapping import WebScraper

def get_index_data(url):
    
    try:
        tables = WebScraper.get_idex_table_from_article(url)

        # Parse the HTML
        soup = BeautifulSoup(tables[0], "html.parser")

        # Remove <h3> and <h5> tags
        for tag in soup.find_all(["h1", "h2",  "h3", "h4", "h5"]):
            tag.decompose()

        # Convert modified HTML to string
        cleaned_html = str(soup)

        html_io = StringIO(cleaned_html)

        # Convert to Pandas DataFrame
        dfs = pd.read_html(html_io)

        # Extract the first table
        df = dfs[0]

        df = df[df['Index'].isin(['NIFTY 50', 'NIFTY Bank', 'NIFTY Midcap Select'])]

        df = df[['Index', 'Value', '%Change']]

        return df

    except Exception as e:
        logging.info({"Error generating table for NIFTY 50 due to:": e})
        return None
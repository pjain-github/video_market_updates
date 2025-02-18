import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_market_highlights():

    try:
        url = "https://economictimes.indiatimes.com/markets/stocks/liveblog"
        headers = {"User-Agent": "Mozilla/5.0"}  # Prevent blocking

        logging.info("Fetching data from URL: %s", url)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error("Failed to fetch data, Status Code: %d", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        today_date = datetime.today().strftime('%d %b %Y')  # Format: '17 Feb 2025'
        logging.info("Looking for market highlights for date: %s", today_date)

        latest_link = None
        latest_text = None

        for story in soup.find_all("div", class_="eachStory"):
            date_tag = story.find("time", class_="date-format")
            if date_tag and today_date in date_tag.text:
                link_tag = story.find("a", href=True)
                if link_tag:
                    latest_link = "https://economictimes.indiatimes.com" + link_tag["href"]
                    latest_text = link_tag.text.strip()
                    logging.info("Found latest market highlight: %s", latest_text)
                    break
                
        if latest_link:
            # return {"title": latest_text, "link": latest_link}
            return latest_link
        else:
            logging.warning("No latest market highlights found.")
            return None
        
    except:
        return None
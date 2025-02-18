import os
from dotenv import load_dotenv
# from search import index, fii_dii, news, recommendation
from data.google_search import GoogleSearch
from ai.gemini_util import Gemini
from ai.audio_util import AudioUtil
from video.merge_video import merge_videos
from pages.index.index import Index
from pages.news.news import News
from pages.stocks.stocks import Stocks
from pages.first_page.first_page import FirstPage
from pages.last_page.last_page import LastPage
import io

load_dotenv()

# Get the API key and CSE ID from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')
google_cse_id = os.getenv('GOOGLE_SEARCH_CSE_ID')
gemini_api_key = os.getenv('GOOGLE_API_KEY')

def main(news_links=None, stocks_links=None):

    gemini = Gemini(api_key=gemini_api_key)
    audioutil = AudioUtil()

    gsc = GoogleSearch(api_key=google_api_key, cse_id=google_cse_id)

    video1 = FirstPage.first_page()

    index_search = Index(google_search_class=gsc, gl='in', llm_class=gemini, audio_class=audioutil) 
    video2 = index_search.index_slide()

    news_search = News(google_search_class=gsc, gl='in', llm_class=gemini, audio_class=audioutil, links=news_links) 
    video3 =  news_search.news_slide()

    stocks_search = Stocks(google_search_class=gsc, gl='in', llm_class=gemini, audio_class=audioutil, links=stocks_links)
    video4 = stocks_search.stocks_slide()

    video5 = LastPage.last_page()

    final_video = merge_videos([video1, video2, video3, video4, video5])

    return final_video

    final_video.write_videofile("output.mp4", fps=30, codec="libx264", threads=4)

# def main():
#     video_io = io.BytesIO()
#     with open('merged_video.mp4', "rb") as f:
#         video_io.write(f.read())
#     video_io.seek(0)
#     return video_io

if __name__ == "__main__":
    main()


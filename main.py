import os
from dotenv import load_dotenv
from search import index, fii_dii, news, recommendation
from data.google_search import GoogleSearch
from ai.gemini_util import Gemini
from ai.audio_util import AudioUtil
from video.complete_simple_video import generate_video

load_dotenv()

# Get the API key and CSE ID from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')
google_cse_id = os.getenv('GOOGLE_SEARCH_CSE_ID')
gemini_api_key = os.getenv('GOOGLE_API_KEY')

def main():

    gemini = Gemini(api_key=gemini_api_key)
    audioutil = AudioUtil()

    gsc = GoogleSearch(api_key=google_api_key, cse_id=google_cse_id)

    index_search = index.IndexSearch(google_search_class=gsc, gl='in', llm_class=gemini, audio_class=audioutil) 
    index_updates, index_image_path, index_audio_path =  index_search.index_updates()

    news_search = news.NewsSearch(google_search_class=gsc, gl='in', llm_class=gemini, audio_class=audioutil) 
    news_updates, news_image_path, news_audio_path =  news_search.news_updates()

    fii_dii_search = fii_dii.FiiDiiSearch(google_search_class=gsc, gl='in', llm_class=gemini, audio_class=audioutil) 
    fii_dii_updates, fii_dii_image_path, fii_dii_audio_path =  fii_dii_search.fii_dii_updates()

    generate_video(
        [index_image_path, news_image_path[0], news_image_path[1],  fii_dii_image_path], 
        [index_audio_path, news_audio_path, fii_dii_audio_path],
        "elements/market_updates.png", "elements/intro_audio.wav", "elements/end_screen.png", "elements/outro_audio.wav", "elements/video.mp4")

    # generate_video(
    #     ['elements/slide_1.png', 'elements/slide_2.png', 'elements/slide_3.png',  'elements/slide_4.png'], 
    #     ['elements/index_updates.wav', 'elements/news_updates.wav', 'elements/fii_dii_updates.wav'],
    #     "elements/market_updates.png", "elements/intro_audio.wav", "elements/end_screen.png", "elements/outro_audio.wav", "elements/video.mp4")


if __name__ == "__main__":
    main()


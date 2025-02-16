from constants import nifty_webistes, nifty_queries, nifty_data, index_data
from pydantic import BaseModel, Field
from typing import List
from data.nifty_data import get_nifty_data
from data.index_table import get_index_data
from pages.index.slides import ImageGenerator
from video.video import create_video_with_audio

class Slide(BaseModel):
    """Slide Details"""
    bullet_points: str = Field(description="Bullet Points for the Slide")
    speech: str = Field(description="Speech for the slide")


class Index:

    def __init__(self, google_search_class, llm_class, audio_class, gl='in'):
        self.gsc = google_search_class
        self.search_websites = nifty_webistes
        self.queries = nifty_queries
        self.gl = gl
        self.llm = llm_class
        self.audio = audio_class
        self.nify_data_websites = nifty_data
        self.index_data_websites = index_data

    def index_slide(self):

        nifty_data = get_nifty_data(self.nify_data_websites[0])
        index_data = get_index_data(self.index_data_websites[0])

        image_generator = ImageGenerator()

        index_table = image_generator.index_df_to_image(index_data)
        nifty_table = image_generator.plot_candlestick_chart(df= nifty_data)

        params = {
            'num': 3,
            'start': 1,
            'lr': 'en',
            'gl': self.gl,
            'safe': 'off',
            'dateRestrict': 'd[1]',
            'sites': self.search_websites,
            'sort': 'date'
        }

        search_results = []
        for query in self.queries:
            search_results.extend(self.gsc.search(query, **params))

        # search_results.extend([{'link':link} for link in self.self.websites])

        results = [self.gsc.process_google_search(search_result) for search_result in search_results]

        answer = self.generate_script(results, index_table)

        nifty_img = image_generator.create_nifty_with_image(heading="Index Movement", image_element=nifty_table, right_top_image=index_table, bullet_list=answer[0])

        audio_path = self.audio.text_to_wav_from_config(answer[1])

        video1 = create_video_with_audio(tts_response=audio_path, image=nifty_img)

        return video1

    def generate_script(self, results, index_table):

        intial_prompt = """
        Prompt for Financial Analyst - NIFTY Update Extraction

        Role: You are a financial analyst responsible for extracting and summarizing key insights from the latest web-scraped NIFTY-related articles and structured market data. Your goal is to generate a structured financial briefing that provides clear and actionable information for market analysis.

        Task Overview:
            Process the provided data, including index values, previous prices, and percentage changes, along with web-scraped articles to generate a structured financial briefing in JSON format. 
        
        The output must include:

        Key Updates (Bullet Points):
            Summarize the most critical insights in a maximum of 3 bullet points.
            Ensure that at least one point provides a general market update on the NIFTY, BANK NIFTY and MIDCAP NIFTY index's movement (e.g., overall gain/loss, percentage change).
            Include notable sector or stock-specific movements that have influenced the index.
            Mention key economic or geopolitical factors impacting the market.
            Avoid redundant or generic statements.
            Bullet points should be in plain format, separated by \\n (not markdown formatting).
        Market Commentary (Speech Format):
            Generate a professional market commentary in the tone of a financial analyst.
            Provide a detailed analysis of index movements, including percentage changes for NIFTY indices (e.g., "Nifty 50 dropped 1.1% yesterday, closing at 19,850.45").
            Contextualize the movement by explaining key drivers (e.g., global market trends, economic data, sector performance, policy changes).
            Ensure the commentary is structured, insightful, and free from generic statements.
            Maintain a formal but engaging tone to make the briefing clear and actionable.
            This is part of a longer financial presentation, so do not add any greetings or salutations, like hi, good morning.
        """
        
        prompt = intial_prompt + f"Index information: {index_table}"
        prompt = prompt + "Webscrapped Articles: \n"

        for result in results:
            if result['content']:
                prompt  = prompt + result['content']

        answer = self.llm.call_llm_json(prompt, Slide)

        answer = self.process_results(answer)

        return answer

        # answer = self.llm.call_llm_json(prompt, Slide)

        # return answer
    
    def process_results(self, results):

        bullet_points = results.bullet_points
         
        if "\\n" in bullet_points:
            bullet_points = bullet_points.split("\\n")
        else:
            bullet_points = bullet_points.split("\n")

        for i in range(len(bullet_points)):
            bullet_points[i] = bullet_points[i].strip()
            if '"' in bullet_points[i]:
                bullet_points[i] = bullet_points[i].replace('"', "")

        return bullet_points, results.speech

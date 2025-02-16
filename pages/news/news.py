from constants import news_webistes, news_queries, news_fixed_links
from pydantic import BaseModel, Field
from typing import List
from pages.news.slides import ImageGenerator
from video.video import create_video_with_audio


# Pydantic
# Define the Description model
class Slide(BaseModel):
    """Slide Details"""
    bullet_points: str = Field(description="Bullet Points for the Slide")
    speech: str = Field(description="Speech for the slide")


class News:

    def __init__(self, google_search_class, llm_class, audio_class,gl='in'):
        self.gsc = google_search_class
        self.websites = news_webistes
        self.queries = news_queries
        self.gl = gl
        self.llm = llm_class
        self.fixed_links = news_fixed_links
        self.audio = audio_class

    def news_slide(self):
        
        params = {
            'num': 5,
            'start': 1,
            'lr': 'en',
            'gl': self.gl,
            'safe': 'off',
            'dateRestrict': 'd[1]',
            'sites': self.websites,
            'sort': 'date'
        }

        search_results = []
        for query in self.queries:
            search_results.extend(self.gsc.search(query, **params))

        search_results.extend([{'link':link} for link in self.fixed_links])

        results = [self.gsc.process_google_search_simple(search_result) for search_result in search_results]

        image_generator = ImageGenerator()

        image = image_generator.convert_image_to_pil("elements/shutterstock_332980589_11zon.webp")

        answer = self.generate_script(results)

        news_img = image_generator.create_slide_with_image(heading="Market Updates", image_element=image, bullet_list=answer[0])

        audio_path = self.audio.text_to_wav_from_config(answer[1])

        video2 = create_video_with_audio(tts_response=audio_path, image=news_img)

        return video2
    
    def generate_script(self, results):

        intial_prompt = """
        Prompt for Financial Analyst - Market Updates Extraction

        Role: You are an Indian financial analyst responsible for extracting and summarizing key insights from the latest web-scraped market news articles. Your goal is to generate structured updates that highlight critical government announcements, macroeconomic and microeconomic indicators, and their potential impact on financial markets.

        Task Overview:
            Process the web-scraped articles and generate a structured financial briefing in JSON format. The output must include:

        Key Updates (Bullet Points):
            Summarize the most critical insights in a maximum of 5 bullet points.
            Focus on government announcements, regulatory changes, monetary and fiscal policies, inflation trends, GDP growth, interest rate changes, foreign exchange movements, trade balances, and sector-specific updates that influence markets.
            Include major updates on taxation, foreign investments, and industry-specific policy changes.
            Do not add any information for a specific stock.
            Avoid redundant or generic information.
            Bullet points should be in plain format, separated by \\n (not markdown formatting).
        
        Market Commentary (Speech Format):
            Generate a professional market commentary in the tone of a financial analyst.
            Provide context and background on the extracted insights, explaining their implications for broader financial markets.
            Discuss how government policies, macroeconomic indicators, and sectoral trends are shaping market movements.
            Ensure the commentary is insightful, structured, and free from generic statements.
            Use a formal but engaging tone to make the briefing clear and actionable.
            The speech should be detailed, analytical, and connect different updates logically.
            This slide and speech are part of a long presentation, so do not include any salutations or greetings, like hi, good morning.

        """

        prompt = intial_prompt + "Webscrapped Articles: \n"

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

        bullet_points = [bp for bp in bullet_points if len(bp) >= 5]

        return bullet_points, results.speech
    




        
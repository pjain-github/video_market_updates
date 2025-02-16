from constants import stocks_webistes, stocks_queries, stocks_fixed_links
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


class Stocks:

    def __init__(self, google_search_class, llm_class, audio_class,gl='in'):
        self.gsc = google_search_class
        self.websites = stocks_webistes
        self.queries = stocks_queries
        self.gl = gl
        self.llm = llm_class
        self.fixed_links = stocks_fixed_links
        self.audio = audio_class

    def stocks_slide(self):
        
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

        stocks_img = image_generator.create_slide_with_image(heading="Stocks In Action", image_element=image, bullet_list=answer[0])

        audio_path = self.audio.text_to_wav_from_config(answer[1])

        video3 = create_video_with_audio(tts_response=audio_path, image=stocks_img)

        return video3
    
    def generate_script(self, results):

        intial_prompt = """
        Prompt for Financial Analyst – Stock Market Updates Extraction
        
        Role:
            You are an Indian financial analyst responsible for extracting and summarizing key insights from the latest web-scraped stock market news. Your goal is to generate structured updates that highlight critical stock-related announcements, market trends, and their potential impact on investors.

        Task Overview:
            Process the web-scraped articles and generate a structured stock market briefing in JSON format. The output must include:

        Key Stock Updates (Bullet Points):
            Summarize the most significant stock-related insights in a maximum of 5 bullet points.
            Focus on corporate earnings, M&A activity, IPOs, share buybacks, dividend declarations, stock splits, regulatory actions, and major company announcements.
            Highlight key movements in benchmark indices (Sensex, Nifty) and sectoral performance.
            Include insights on foreign and domestic institutional investor (FII/DII) activity impacting the stock market.
            Do not include generic market commentary or macroeconomic updates unless directly linked to stock market movements.
            Bullet points should be in plain format, separated by \n (not markdown formatting).
        
        Market Commentary (Speech Format):
            Generate a professional stock market commentary in the tone of a financial analyst.
            Provide context and background on key stock-related insights, explaining their implications for investors.
            Discuss market movements, investor sentiment, and how major stock-specific announcements are influencing broader market trends.
            Ensure the commentary is analytical, structured, and free from generic statements.
            Use a formal but engaging tone to make the briefing clear and actionable.
            This commentary is part of a longer financial presentation, so do not include any salutations or greetings like hi, good morning.
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
     
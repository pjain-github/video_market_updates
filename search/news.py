from constants import news_webistes, news_queries, news_fixed_links
from pydantic import BaseModel, Field
from typing import List
from image.combine_img import generate_element_images_without_table


# Pydantic
# Define the Description model
class Slide(BaseModel):
    """Slide Details"""
    bullet_points: str = Field(description="Bullet Points for the Slide")
    speech: str = Field(description="Speech for the slide")


class NewsSearch:

    def __init__(self, google_search_class, llm_class, audio_class,gl='in'):
        self.gsc = google_search_class
        self.websites = news_webistes
        self.queries = news_queries
        self.gl = gl
        self.llm = llm_class
        self.fixed_links = news_fixed_links
        self.audio = audio_class

    def news_updates(self):
        
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

        answer = self.generate_script(results)

        image_path = self.process_results(answer)
        
        audio_path = self.audio.text_to_wav_from_config(answer.speech, "elements/news_updates.wav")
        
        return answer, image_path, audio_path
    
    def generate_script(self, results):

        intial_prompt = """
        Prompt for Financial Analyst - News Extraction
        Role: You are an Indian financial analyst responsible for extracting and summarizing key insights from the latest web-scraped market news related articles. Your goal is to generate structured updates that provide clear and actionable information for market analysis.

        Task Overview:
            Process the web-scraped articles and generate a structured financial briefing in JSON format. 
            First 6 points should mention general market updates like governemt schemes, SIP data, market outlook.
            Last 6 points should focus on indian stocks update/news. 
            Do not dedicate more than 2 bullet points for one stock/news item. 
            The output must include:

        Key Updates (Bullet Points):
            Summarize the most critical insights in a maximum of 12 bullet points.
            Each point should be short, direct, and focused on market-moving events (e.g., index trends, major stock movements, economic policies affecting markets).
            Avoid redundant or generic information.
            Bullet points should be plain format, not markdown formatting, seperate each bullet points by "\\n"
        
        Market Commentary (Speech Format):
            Generate a professional market commentary in the tone of a financial analyst.
            Provide context and background on the extracted insights, explaining their impact on broader financial markets.
            Ensure that the commentary is insightful, structured, and free from generic statements.
            Use a formal but engaging tone to make the briefing clear and actionable.
            This slide and speech is a part of long presentation, so do not use any salution or greeting.
            The speech should contain detail.

        """

        prompt = intial_prompt + "Webscrapped Articles: \n"

        for result in results:
            if result['content']:
                prompt  = prompt + result['content']

        answer1 = self.llm.call_llm_json(prompt, Slide)
        answer2 = self.llm.call_llm_json(prompt, Slide)

        combined_prompt = """

        You are given results from two function, use the results to complete the task
        """

        combined_prompt = combined_prompt + intial_prompt

        combined_prompt += answer1.bullet_points  + answer1.speech
        combined_prompt += answer2.bullet_points  + answer2.speech

        final_answer = self.llm.call_llm_json(combined_prompt, Slide)

        print(final_answer)

        return final_answer

        # for result in results:
        #     if result['content']:
        #         prompt  = prompt + result['content']

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

        if len(bullet_points) > 6:
            bullet_points_1 = bullet_points[:6]
            bullet_points_2 = bullet_points[6:]
        else:
            bullet_points_1 = bullet_points
            bullet_points_2 = None

        speeches = results.speech

        slide_2 =  generate_element_images_without_table(bullet_points_1, "News Updates", "elements/slide_2.png")
        if bullet_points_2:
            slide_3 =  generate_element_images_without_table(bullet_points_2, "News Updates", "elements/slide_3.png")
        else:
            slide_3 = None

        return slide_2, slide_3
    




        
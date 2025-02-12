from constants import nifty_webistes, nifty_queries
from pydantic import BaseModel, Field
from typing import List
from image.combine_img import generate_element_images


# Pydantic
# Define the Description model
class Slide(BaseModel):
    """Slide Details"""
    bullet_points: str = Field(description="Bullet Points for the Slide")
    table: str = Field(description="HTML code for table in the slide")
    speech: str = Field(description="Speech for the slide")


class IndexSearch:

    def __init__(self, google_search_class, llm_class, audio_class, gl='in'):
        self.gsc = google_search_class
        self.search_websites = nifty_webistes
        self.queries = nifty_queries
        self.gl = gl
        self.llm = llm_class
        self.audio = audio_class
        # self.websites = nifty_webistes_list

    def index_updates(self):
        
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

        answer = self.generate_script(results)

        image_path = self.process_results(answer)

        audio_path = self.audio.text_to_wav_from_config(answer.speech, "elements/index_updates.wav")
        
        return answer, image_path, audio_path
    
    def generate_script(self, results):

        intial_prompt = """
        Prompt for Financial Analyst - NIFTY Update Extraction
        Role: You are a financial analyst responsible for extracting and summarizing key insights from the latest web-scraped NIFTY-related articles. Your goal is to generate structured updates that provide clear and actionable information for market analysis.

        Task Overview:
            Process the web-scraped articles and generate a structured financial briefing in JSON format. The output must include:

        Key Updates (Bullet Points):
            Summarize the most critical insights in a maximum of 4 bullet points.
            Each point should be direct, and focused on market-moving events (e.g., index trends, major stock movements, economic policies affecting NIFTY).
            Avoid redundant or generic information.
            Bullet points should be plain format, not markdown formatting, seperate each bullet points by "\\n"
        
        Market Data (HTML Table - If Applicable):
            Extract any numerical data such as index values, stock movements, percentage changes, financial metrics, etc.
            Convert the extracted data into a single well-formatted HTML table for easy reference.
            Ensure correct alignment of figures and headings.
            If no numerical data is available, set this field to null.
            Table width should be less than 250 px and height less than 350px
        
        Market Commentary (Speech Format):
            Generate a professional market commentary in the tone of a financial analyst.
            Provide context and background on the extracted insights, explaining their impact on NIFTY and broader financial markets.
            Ensure that the commentary is insightful, structured, detailed and free from generic statements.
            Use a formal but engaging tone to make the briefing clear and actionable.
            This slide and speech is a part of long presentation, so do not use any salution or greeting.
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

        combined_prompt += answer1.bullet_points + answer1.table + answer1.speech
        combined_prompt += answer2.bullet_points + answer2.table + answer2.speech

        final_answer = self.llm.call_llm_json(combined_prompt, Slide)

        return final_answer

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

        table = results.table

        return generate_element_images(bullet_points, table, "Index Updates", "elements/slide_1.png")



        



        
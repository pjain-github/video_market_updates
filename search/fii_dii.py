from constants import fii_dii_webistes, fii_dii_queries, fii_dii_fixed_links
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


class FiiDiiSearch:

    def __init__(self, google_search_class, llm_class, audio_class, gl='in'):
        self.gsc = google_search_class
        self.websites = fii_dii_webistes
        self.queries = fii_dii_queries
        self.gl = gl
        self.llm = llm_class
        self.fixed_links = fii_dii_fixed_links
        self.audio = audio_class

    def fii_dii_updates(self):
        
        params = {
            'num': 3,
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

        results = [self.gsc.process_google_search(search_result) for search_result in search_results]

        answer = self.generate_script(results)

        image_path = self.process_results(answer)
        
        audio_path = self.audio.text_to_wav_from_config(answer.speech, "elements/fii_dii_updates.wav")
        
        return answer, image_path, audio_path
    
    def generate_script(self, results):

        intial_prompt = """
        Role: You are a financial analyst responsible for extracting and summarizing key insights from the latest FII (Foreign Institutional Investors) and DII (Domestic Institutional Investors) trading data. Your goal is to generate a structured financial briefing that provides clear and actionable insights into institutional investor activity, its impact on the market, and future expectations.

        Task Overview:
            Process the latest FII and DII trading data and generate a structured financial briefing in JSON format. The output must include:

        1. Key Updates (Bullet Points):
            Summarize the most critical insights in a maximum of 4 bullet points.
            Each point should be short, direct, and focused on market-moving trends related to FII & DII flows.
            Cover aspects such as:
            Net buying or selling by FIIs and DIIs.
            Key sectors or stocks seeing strong institutional activity.
            Any unusual trends or shifts in investment patterns.
            Expected short-term market impact based on institutional flows.
            Avoid redundant or generic information.
            Bullet points should be plain format, not markdown formatting, seperate each bullet points by "\\n"

        2. Institutional Trading Data (HTML Table):
            Extract and present FII and DII trading activity, including:
            FII Bought (Total value of stocks purchased by FIIs).
            FII Sold (Total value of stocks sold by FIIs).
            DII Bought (Total value of stocks purchased by DIIs).
            DII Sold (Total value of stocks sold by DIIs).
            Convert the extracted data into a well-formatted HTML table for easy reference.
            Ensure correct alignment of figures and headings.
            If no numerical data is available, set this field to null.
            Table width should be less than 250 px and height less than 350px

        3. Market Commentary (Speech Format):
            Provide a professional market commentary analyzing institutional trading trends.
            Explain how FII & DII flows are influencing market sentiment and broader indices.
            Discuss potential sectoral movements based on institutional positioning.
            Offer expectations for the upcoming trading sessions, considering trends, global factors, and investor sentiment.
            Ensure that the commentary is insightful, structured, and free from generic statements.
            Maintain a formal but engaging tone, making the briefing actionable for traders and analysts.
            This slide and speech is a part of a long presentation, so do not include any salutation or greeting.

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

        table = results.table
        speeches = results.speech

        return generate_element_images(bullet_points, table, "FII-DII Updates", "elements/slide_4.png")




        
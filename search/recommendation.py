from constants import recommendation_webistes, recommendation_queries
from pydantic import BaseModel, Field
from typing import List
from image.combine_img import generate_element_images_without_bullet_points


# Pydantic
# Define the Description model
class Slide(BaseModel):
    """Slide Details"""
    table: str = Field(description="HTML code for table in the slide")
    speech: str = Field(description="Speech for the slide")


class RecommendationSearch:

    def __init__(self, google_search_class, llm_class, gl='in'):
        self.gsc = google_search_class
        self.websites = recommendation_webistes
        self.queries = recommendation_queries
        self.gl = gl
        self.llm = llm_class

    def recommendation_updates(self):
        
        params = {
            'num': 7,
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

        results = [self.gsc.process_google_search_simple(search_result) for search_result in search_results]

        answer = self.generate_script(results)

        image_path = self.process_results(answer)
        
        return answer, image_path
    
    def generate_script(self, results):

        intial_prompt = """
        Prompt: Financial Analyst - Stock Market Recommendations Extraction
        Role: You are a financial analyst responsible for extracting and summarizing the latest stock market recommendations from web-scraped sources. Your goal is to generate a structured financial briefing that provides actionable stock insights, including expert verdicts on whether to buy or sell specific stocks, along with reasoning and source attribution.

        Task Overview:
            Process the latest stock market recommendations and generate a structured financial briefing in JSON format. The output must include:

        1. Stock Recommendations Table (HTML Table):
            Extract and present expert stock recommendations, including:
            Stock Name: The name of the stock being recommended.
            Verdict: "Buy" or "Sell" recommendation based on expert analysis.
            Why? (Reason to Buy/Sell): The key reasoning behind the recommendation, such as earnings growth, sector outlook, valuation, or technical factors.
            Source: The website, analyst, or financial institution recommending the stock.
            Buying/Selling price: The recommended price range for buying or selling the stock. (if available)
            Convert the extracted data into a well-formatted HTML table for easy reference.
            Ensure correct alignment of figures and headings.
            If no recommendations are available, set this field to null.
            Table width should be less than 600px and height less than 350px
        2. Market Commentary (Speech Format):
            Provide a professional stock market commentary analyzing the key takeaways from expert recommendations.
            Discuss the rationale behind buy and sell calls, linking them to market trends, economic indicators, or sector-specific insights.
            Offer insights into how these recommendations align with broader market sentiment and expected trends.
            Ensure that the commentary is insightful, structured, and free from generic statements.
            Maintain a formal but engaging tone, making the briefing actionable for investors.
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

        combined_prompt += answer1.table + answer1.speech
        combined_prompt += answer2.table + answer2.speech

        final_answer = self.llm.call_llm_json(combined_prompt, Slide)

        return final_answer

        # for result in results:
        #     if result['content']:
        #         prompt  = prompt + result['content']

        # answer = self.llm.call_llm_json(prompt, Slide)

        # return answer
    
    def process_results(self, results):

        table = results.table
        speeches = results.speech

        return generate_element_images_without_bullet_points(table_html=table, heading_text="Stock Recommendations", output_path="slide_4.png")




        
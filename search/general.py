from constants import nifty_webistes, nifty_queries
from pydantic import BaseModel, Field
from typing import List


# Pydantic
# Define the Description model
class Slide(BaseModel):
    """Slide Details"""
    bullet_points: str = Field(description="Bullet Points for the Slide")
    table: str = Field(description="HTML code for table in the slide")
    speech: str = Field(description="Speech for the slide")


class IndexSearch:

    def __init__(self, google_search_class, llm_class, gl='in'):
        self.gsc = google_search_class
        self.gl = gl
        self.llm = llm_class

    def index_updates(self):
        
        params = {
            'num': 5,
            'start': 1,
            'lr': 'en',
            'gl': self.gl,
            'safe': 'off',
            'sort': 'date'
        }

        search_results = []
        for query in self.queries:
            search_results.extend(self.gsc.search(query, **params))

        results = [self.gsc.process_google_search(search_result) for search_result in search_results]

        answer = self.generate_script(results)
        
        return answer
    
    def generate_script(self, results):

        prompt = """
        Prompt for Financial Analyst - NIFTY News Extraction
        Role: You are a financial analyst responsible for extracting and summarizing key insights from the latest web-scraped NIFTY-related articles. Your goal is to generate structured updates that provide clear and actionable information for market analysis.

        Task Overview:
            Process the web-scraped articles and generate a structured financial briefing in JSON format. The output must include:

        Key Updates (Bullet Points):
            Summarize the most critical insights in a maximum of 4 bullet points.
            Each point should be short, direct, and focused on market-moving events (e.g., index trends, major stock movements, economic policies affecting NIFTY).
            Avoid redundant or generic information.
        
        Market Data (HTML Table - If Applicable):
            Extract any numerical data such as index values, stock movements, percentage changes, financial metrics, etc.
            Convert the extracted data into a single well-formatted HTML table for easy reference.
            Ensure correct alignment of figures and headings.
            If no numerical data is available, set this field to null.
        
        Market Commentary (Speech Format):
            Generate a professional market commentary in the tone of a financial analyst.
            Provide context and background on the extracted insights, explaining their impact on NIFTY and broader financial markets.
            Ensure that the commentary is insightful, structured, and free from generic statements.
            Use a formal but engaging tone to make the briefing clear and actionable.
            This slide and speech is a part of long presentation, so do not use any salution or greeting.

        Webscrapped Aricles: 
        """

        for result in results:
            if result['content']:
                prompt  = prompt + result['content']

        answer = self.llm.call_llm_json(prompt, Slide)

        return answer



        
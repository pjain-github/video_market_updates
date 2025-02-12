nifty_webistes = None#['www.moneycontrol.com', 'www.nseindia.com', 'https://www.livemint.com/']
nifty_queries = ["nifty updates"]

news_webistes = ['economictimes.indiatimes.com', 'www.moneycontrol.com', 'https://www.livemint.com/']
news_queries = ["latest news on stocks"]
news_fixed_links = ['https://www.moneycontrol.com/news/business/markets/', 'https://economictimes.indiatimes.com/markets/stocks/live-blog/bse-sensex-today-live-nifty-stock-market-updates-11-february-2025/liveblog/118131028.cms']

fii_dii_webistes = None
fii_dii_queries = ["fii and dii news"]
fii_dii_fixed_links = ['https://www.nseindia.com/reports/fii-dii']

post_market_webistes = None
post_market_queries = ["post market analysis"]

recommendation_webistes = None
recommendation_queries = ["stock market recommendations"]

audio_config = {
    "audioConfig": {
        "audioEncoding": "LINEAR16",
        "effectsProfileId": [
            "small-bluetooth-speaker-class-device"
        ],
        "pitch": -4,
        "speakingRate": 1.2
    },
    "input": {
        "text": "Sample Input Text"
    },
    "voice": {
        "languageCode": "en-US",
        "name": "en-US-Standard-A"
    }
}

intital_prompt = """Hi, welcome to Fin Insights AI. Here's your daily Indian stock market update, powered by AI."""

final_prompt = """That's all for this video. Subscribe to our channel for the latest financial updates and analysis by AI. Thank you for listening!"""
import streamlit as st
from main import main

nifty_webistes = None#['www.moneycontrol.com', 'www.nseindia.com', 'https://www.livemint.com/']
nifty_queries = ["nifty updates"]
nifty_data = ['https://www.equitypandit.com/share-price/today/nifty-50-historical-data']
index_data = ['https://www.livemint.com/market/india-indices-nse']

news_webistes = ['economictimes.indiatimes.com', 'www.moneycontrol.com', 'https://www.livemint.com/']
news_queries = ["market accounements"]
news_fixed_links = ['https://www.moneycontrol.com/news/business/markets/', 'https://economictimes.indiatimes.com/markets/stocks/live-blog/bse-sensex-today-live-nifty-stock-market-updates-14-february-2025/liveblog/118230190.cms']

stocks_webistes = ['economictimes.indiatimes.com', 'www.moneycontrol.com', 'https://www.livemint.com/']
stocks_queries = ["market accounements"]
stocks_fixed_links = ['https://www.moneycontrol.com/news/business/markets/', 'https://economictimes.indiatimes.com/markets/stocks/live-blog/bse-sensex-today-live-nifty-stock-market-updates-14-february-2025/liveblog/118230190.cms']

st.title("Streamlit Video Generator")

with st.expander("News (Input Text or Website)"):
    news_input = st.text_area("Enter news website or text", value="")
    news_terms = st.text_input("Enter search terms for news", value="")
    if news_input!="":
        news_fixed_links = [news_input]
    if news_terms!="":
        news_queries = [news_terms]

with st.expander("Stocks (Input Text or Website)"):
    stocks_input = st.text_area("Enter stock website or text", value="")
    stocks_terms = st.text_input("Enter search terms for stocks", value="")
    if stocks_input!="":
        stocks_fixed_links = [stocks_input]
    if stocks_terms!="":
        stocks_queries = [stocks_terms]

with st.expander("Index (Search Terms)"):
    index_terms = st.text_input("Enter search terms for index", value="")
    if index_terms!="":
        nifty_queries = [index_terms]

if st.button("Generate Video"):
    st.write("Generating video... Please wait.")
    video_file = main(news_links=news_fixed_links , stocks_links=stocks_fixed_links)
    st.video(video_file)


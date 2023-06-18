from langchain.document_loaders import UnstructuredHTMLLoader
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import logging

# Set up logging to a file with UTF-8 encoding
log_file = 'my_log_file.log'
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)

# Uncomment the code block below if you want to scrape LinkedIn data
"""
url = "https://www.linkedin.com/in/wilsonlimsetiawan/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
plain_text = soup.get_text()
print(plain_text)
"""

# Scrape tweets using sntwitter
scraper = sntwitter.TwitterSearchScraper("@chrispramana")
tweets = []
for i, tweet in enumerate(scraper.get_items()):
    data = [
        tweet.date,
        #tweet.id,
        tweet.content,
        tweet.user.username,
        tweet.likeCount,
        #tweet.retweetCount,
    ]
    tweets.append(data)
    print(data)
    if i > 50:
        break

tweet_df = pd.DataFrame(tweets, columns=['Datetime', 'Text', 'Username', 'Likes'])

# Log the tweet dataframe
logging.info(f'Tweet DataFrame:\n{tweet_df}')

from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

# Instantiate a LLM
llm = OpenAI(api_token="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")

pandas_ai = PandasAI(llm)

# Log the prompt and run pandas_ai
prompt = 'has chrispramana been to SF before?'
logging.info(f'Prompt: {prompt}')
pandas_ai(tweet_df, prompt=prompt)

from langchain.document_loaders import UnstructuredHTMLLoader
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import logging

# Set up logging to a file with UTF-8 encoding
log_file = 'twitter.log'
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)

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
try:
    prompt = 'You are a talk show host and youre about to interview a very famous startup founder. Based on the tweets of this person, generate three potential interesting questions that a wide range of people might find interesting.'
    logging.info(f'Prompt: {prompt}')
    #pandas_ai(tweet_df, prompt=prompt)
    #print(pandas_ai(tweet_df, prompt=prompt))
    ans = pandas_ai(tweet_df, prompt=prompt)
    print(f'ans: {ans}')
except Exception:
    logging.exception("Exception occurred")
finally:
    print("Done")

from langchain.document_loaders import UnstructuredHTMLLoader
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import logging
import re
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import AnalyzeDocumentChain
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.llms import OpenAI
import os
from langchain.text_splitter import CharacterTextSplitter
log_file = 'article.log'
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)
openai_api_key = "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"
os.environ["OPENAI_API_KEY"] = "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"
def scrape(url):
    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url)
    html_content = response.content
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    for ad in soup.find_all(class_='advertisement'):
        ad.extract()
    # Extract the main content area by selecting specific HTML tags or classes
    # Example: Extract content from a specific tag with class name
    main_content = soup.find(class_='article-content')
    # Clean up the extracted content
    clean_text = main_content.get_text(separator='\n')
    # Remove extra whitespace and newlines
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def summarise(scraped):
    text_splitter = CharacterTextSplitter()
    chunks = text_splitter.split_text(scraped)

    summary_chain = load_summarize_chain(OpenAI(temperature=0),
                                            chain_type="map_reduce",verbose=True)
            
    summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

    answer = summarize_document_chain.run(chunks)
    return answer

url = 'https://techcrunch.com/2021/09/05/singapore-based-caregiving-startup-homage-raises-30m-series-c/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAJPl9ewGP8Q6BDiQ3gAKTFqtucPF7IHWeLvvCbsr5rVm3K_pB70zbBssEOXan2VfI5TTFN2q8vbj_qcchBqjO3zEyRB_XEJ8sfzTjD8f2RX0qIIKJPHrO7NhV65xgjV4YEtOL_LRKVC2KPvfG6ycxATxOE3u9_hKEqMtiv-Zh8XF'
scraped = scrape(url)
summary = summarise(scraped)
print(summary)
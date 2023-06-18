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

# Set up logging to a file with UTF-8 encoding
 #os.environ["OPENAI_API_KEY"] = user_api_key

openai_api_key = "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"
os.environ["OPENAI_API_KEY"] = "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"
user_api_key = "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"
log_file = 'youtube.log'
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)
def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#]+", url)
        if match :
            video_id = match.group()
        else : 
            match = re.search(r"(?<=youtu.be/)[^&#]+", url)
            if match :
                video_id = match.group()
        return video_id
video_url = "https://www.youtube.com/watch?v=UYOwweziqGI"
if video_url :
        video_id = get_youtube_id(video_url)

        if video_id != "":
            t = YouTubeTranscriptApi.get_transcript(video_id, languages=('en','fr','es', 'zh-cn', 'hi', 'ar', 'bn', 'ru', 'pt', 'sw' ))
            finalString = ""
            for item in t:
                text = item['text']
                finalString += text + " "

            text_splitter = CharacterTextSplitter()
            chunks = text_splitter.split_text(finalString)

            summary_chain = load_summarize_chain(OpenAI(temperature=0),
                                            chain_type="map_reduce",verbose=True)
            
            summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

            answer = summarize_document_chain.run(chunks)
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
from dotenv import load_dotenv

def youtube(youtube_url):
    load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    log_file = 'logs/youtube.log'
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
    if youtube_url:
            video_id = get_youtube_id(youtube_url)
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
                print(f'ans: {answer}')

youtube_url = 'https://www.youtube.com/watch?v=UYOwweziqGI'
youtube(youtube_url)
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

import sys
sys.path.append('src/')

from article import article
from twitter import twitter
from youtube import youtube

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'Message': 'Hello there 👋'})

@app.route('/formData', methods=['POST'])
def form_data():
    url = request.form.to_dict()['url']
    print(f'url: {url}')
    # Regex patterns for YouTube, Twitter, and article links
    youtube_pattern = re.compile(r'^(https?:\/\/)?(www\.)?youtube\.com')
    twitter_pattern = re.compile(r'^@')

    if youtube_pattern.match(url):
        return youtube(url)
    elif twitter_pattern.match(url):
        return twitter(url)
    else:
        return article(url)
    
    # add_to_question_bank(article(article_url))
    # add_to_question_bank(twitter(twitter_url))
    # add_to_question_bank(youtube(youtube_url))

    return jsonify({'Url': url})

@app.route('/query')
def query():
    return jsonify(list({'Question 1', 'Question 2'}))

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
sys.path.append('src/')

from twitter import twitter

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'Message': 'Hello there 👋'})

@app.route('/formData', methods=['POST'])
def form_data():
    questionBank = []
    d = request.form.to_dict()
    print(d)
    name = d['name']
    twitter_url = d['twitter_url']
    twitter_res = twitter(twitter_url)
    print(f'String: {twitter_res}')
    return jsonify({'Name': name, 'Question': twitter_res})

@app.route('/query')
def query():
    return jsonify(list({'Question 1', 'Question 2'}))

if __name__ == '__main__':
    app.run()

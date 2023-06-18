from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'Message': 'Hello there 👋'})

@app.route('/formData', methods=['POST'])
def form_data():
    print(request.form)
    name = request.form.get('name')
    twitter_url = request.form.get('twitterUrl')
    print(f'Name: ${name}, Twitter: ${twitter_url}')
    return jsonify({'Name': name, 'twitter_url': twitter_url})

@app.route('/query')
def query():
    return jsonify(list({'Question 1', 'Question 2'}))

if __name__ == '__main__':
    app.run()

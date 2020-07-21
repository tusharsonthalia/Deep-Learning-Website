from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'hello!'

@app.route('/sentimentApi', methods=['POST'])
def sentimentApi():
    """
    POST
    input:
    {'text': "some text to classify"}
    output:
    {
        'result': "neg",
        'probabilty': 0.42,
        'text': "the original text"
    }
    """
    data = request.get_json(force=True)
    text = data['text']
    return jsonify(result="negative", prob=0.42, text="original text")

if __name__ == '__main__':
    a = 1
    if a == None:
        app.run(debug=True)

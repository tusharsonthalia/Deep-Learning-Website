from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_bootstrap import Bootstrap
import models

app = Flask(__name__) # initialising the flask application
nav = Nav(app) # initialising the navigation element
Bootstrap(app) # formatting the webpage using Bootstrap

nav.register_element('navbar', Navbar('Demos:',
    View('Home', 'index'),
    View('Sentiment', 'sentiment')
    ))

@app.route('/')
def homepage():
    # Function to render the homepage
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

@app.route('/sentiment', methods = ['GET', 'POST'])
def sentiment():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        result = models.sentiment(text)
    return render_template('sentiment.html', result=result)

if __name__ == '__main__':
    a = 1
    if a == None:
        app.run(debug=True)

from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_bootstrap import Bootstrap
import requests
import models
app = Flask(__name__)  # initialising the flask application
nav = Nav(app)  # initialising the navigation element
Bootstrap(app)  # formatting the webpage using Bootstrap

nav.register_element('navbar', Navbar('Demos:',
                                      View('Home', 'index'),
                                      View('Sentiment', 'sentiment')
                                      ))
@app.route('/')
def index():
    # Function to render the homepage
    return render_template('index.html')


@app.route('/sentimentApi', methods=['POST'])
def sentimentApi():
    data = request.get_json(force=True)
    text = data['text']
    return jsonify(result="negative", prob=0.42, text="original text")


@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        url = "http://localhost:5000/sentimentApi"
        data = {'text': text}
        result = requests.post(url, json=data).text
        result = result['result']
    return render_template('sentiment.html', result=result)

# @app.route('/cnnApi', methods=['POST'])
# def cnnApi():`
#     data = request.get_json(force=True)


@app.route('/cnn', methods=['GET', 'POST'])
def cnn():
    result = ""
    if request.method == 'POST':
        image = request.form['image']
        result = models.cnn(image)
    res = np.random.choice([])
    return render_template('cnn.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)

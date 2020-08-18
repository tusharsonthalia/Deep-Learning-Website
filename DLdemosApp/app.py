# flask related packages:
from flask import Flask, request, render_template, jsonify, redirect
from flask_restful import Resource, Api
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_bootstrap import Bootstrap

# logging
import logging
from logging.handlers import RotatingFileHandler

# python packages
import numpy as np
#from werkzeug.utils import secure_filename
import base64
import requests
import json
from PIL import Image
import io
import os
import urllib.parse

# Keras
import keras
from keras import backend as K 
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing import sequence

app = Flask(__name__)
nav = Nav(app)
api = Api(app)
Bootstrap(app)

logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Load CNN cats and dogs model
global cnd 
app.logger.info("loading model CND ...")
cnd = load_model('VGG16_cats_and_dogs.h5')
cnd._make_predict_function()
app.logger.info("... model loaded")

# # Load LSTM IMDB sentiment classification model
# global imdb
# app.logger.info("loading model IMDB ...")
# imdb = load_model('imdb.h5')
# imdb._make_predict_function()
# app.logger.info("... model loaded")

# navigation bar (navbar) registration
nav.register_element('navbar', Navbar('Demos:',
    View('Home', 'index'),
    View('CNN', 'cnn'),
    View('Sentiment', 'sentiment'),
    View('Summarize', 'summarize'),
    View('Similarity', 'similarity'),
    View('ChatBot', 'chatbot')
))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

def preprocess_image(image, target_size):
    app.logger.info("CNN API: preprocessing image")
    if image.mode != "RGB":
        app.logger.info("CNN API: converting image to RGB")
        image = image.convert("RGB")
    else:
        app.logger.info("CNN API: received RGB image")
    app.logger.info("CNN API: resizing image to", target_size)
    image = image.resize(target_size)
    app.logger.info("CNN API: converting image to array")
    image = img_to_array(image)
    app.logger.info("CNN API: expanding dimensions")
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/cnnApi', methods=['POST'])
def cnnApi():
    data = request.form.to_dict(flat=False)
    #app.logger.info("CNN API received POST request with data:", data)
    image_base64 = data['image'][0]
    app.logger.info(" CND API: image base64:", image_base64)
    image_binary = base64.b64decode(image_base64)
    app.logger.info(" CND API: image binary:", image_binary)
    image = Image.open(io.BytesIO(image_binary))
    image_processed = preprocess_image(image, target_size=(224, 224))
    app.logger.info(" CND API: image processed:", image_processed)
    prediction = cnd.predict(image_processed).tolist()
    app.logger.info(" CND API: prediction:", prediction)
    return jsonify({'dog':prediction[0][0], 'cat': prediction[0][1]})

app.config["IMAGE_UPLOADS"] = "/Users/navnitbelur/data/startechAI/training/src/apps/DLdemos/static/images"
@app.route('/cnn', methods=['GET', 'POST'])
def cnn():
    res = ""
    filename = ""
    data = ""
    if request.method == "POST":
        # file upload and display
        if request.files:
            image = request.files['image']
            filename = image.filename
            file = os.path.join(app.config["IMAGE_UPLOADS"], filename)
            app.logger.info(" CND webapp: uploading image file:", file)
            image.save(file)
            app.logger.info(" CND webapp: image saved successfully")

        url = "http://localhost:5000/cnnApi" # API endpoint
        b64img = ""
        with open (file, "rb") as f:
            b64img = base64.b64encode(f.read())
        data = {'image': b64img}
        app.logger.info(" CND webapp: sending POST request with data: ...\n", data)
        res = requests.post(url, data).text
        app.logger.info(" CND webapp: received POST response:", res)
    return render_template('cnn.html', result=res, filename=filename)

def preprocess_text(text):
    text_processed = ""
    return text_processed

@app.route('/sentimentApi', methods=['POST'])
def sentimentApi():
    #data = request.get_json(force=True)
    data = request.form.to_dict(flat=False)
    app.logger.info(" Sentiment API: received POST request with data:", data)
    text = data['text'][0]
    app.logger.info(" Sentiment API: extracted text from data:", text)
    text_processed = preprocess_text(text)
    prediction = imdb.predict(text_processed).tolist()
    return jsonify({'res':"0.5"})
    
@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    res = ""
    if request.method == "POST":
        text = request.form['text']
        url = "http://localhost:5000/sentimentApi"
        data = {'text': text}
        app.logger.info(" Sentiment webapp: sending POST request with data:\n", data)
        res = requests.post(url, data).text
        app.logger.info(" Sentiment webapp: received POST response:", res)
    return render_template('sentiment.html', result=res)

@app.route('/summarizeApi', methods=['POST'])
def summarizeApi():
    data = request.get_json(force=True)
    text = data['text']
    summary = "this is a hard-coded summary"
    return jsonify(result=summary, text=text)

@app.route('/summarize')
def summarize():
    return render_template('summarize.html')

@app.route('/similarity')
def similarity():
    return render_template('similarity.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == "__main__":
    # enable logging
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHanler(handler)
    # run the app
    app.run(debug=True)
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello!'


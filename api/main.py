#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import jsonify
from yoloid import img_detector

app = Flask(__name__)

@app.route("/")
def index():
    return "Usage: obj-det"

@app.route("/api/<path:url>")
def api(url):
    datas = img_detector(url)
    return jsonify(datas)

app.run(host="0.0.0.0")

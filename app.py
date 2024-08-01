import os
import io
from flask import Flask, render_template, request, flash, redirect, jsonify, make_response, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
# import subprocess
# import sys
# import time
# import audio_processing
# from pydub import AudioSegment # install ffmpeg first
import pandas as pd
import csv
import json

app = Flask(__name__, template_folder='templates/')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# print('upload folder:', os.path.abspath(UPLOAD_FOLDER))
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER) 

app.config['DATA_FOLDER'] = DATA_FOLDER

# Checks so file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')      
def index(): 
    return render_template('index.html')

# @app.route('/audio-files', methods=['POST'])
# def upload_file():
#     if formData not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['audio']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     filename = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filename)
#     return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/remixer')
def load_features_csv():
    filename = os.path.join(DATA_FOLDER, 'data.csv')
    data = pd.read_csv(filename, header=0)
    feed_data = list(data.values) # 32 * 
    return render_template('audio_viz.html', feed_data=feed_data)

@app.route('/data/<path:subpath>', methods=['GET']) # <string:filename> not working for path
def get_file(subpath=''):
    return send_file(os.path.join(DATA_FOLDER, subpath))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
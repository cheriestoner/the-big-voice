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
import csv
import json

app = Flask(__name__, template_folder='templates/')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# print('upload folder:', os.path.abspath(UPLOAD_FOLDER))
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')      
def index(): 
    return render_template('index.html')

@app.route('/audio-files', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return jsonify({"message": "File uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(port=3000)

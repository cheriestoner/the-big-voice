import os
import io
from flask import Flask, render_template, request, flash, redirect, jsonify, make_response, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
# import subprocess
# import sys
# import time
import pandas as pd
import csv
import json
import logging
logging.basicConfig(level=logging.DEBUG)
import audio_processing

app = Flask(__name__, template_folder='templates/')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'audio')
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
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

@app.route('/remix/<string:filename>')
def process_features(filename):
    # filename = os.path.join(DATA_FOLDER, 'test_office/xyz.csv')
    # data = pd.read_csv(filename, header=0)
    # feed_data = data.values.tolist() # 32 * 
    if os.path.exists(os.path.join(DATA_FOLDER, filename[:-4])):
        app.logger.info("Data exist!")
    else:
        audio_processing.main(filename, AUDIO_FOLDER, DATA_FOLDER)
    return render_template('audio_viz.html', audiofile=filename[:-4])

@app.route('/loading/<string:filename>', methods=['GET', 'POST'])
def loading_page(filename):
    return render_template('loading_xh.html', filename=filename) # or change it to loading_jy.html

@app.route('/data/<path:subpath>', methods=['GET']) # <string:filename> not working for path
def get_file(subpath=''):
    return send_file(os.path.join(DATA_FOLDER, subpath))

@app.route('/audio/<path:subpath>', methods=['GET', 'POST'])
def get_audio(subpath=''):
    return send_file(os.path.join(AUDIO_FOLDER, subpath))

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        app.logger.error('No file part')
        return jsonify({'error': 'No file part'})
    file = request.files['audio']
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify({'error': 'No selected file'})
    if file:
        file_path = os.path.join(AUDIO_FOLDER, file.filename) # save to AUDIO_FOLDER
        file.save(file_path)
        file.close()
        app.logger.info(f'File saved to {file_path}')
        # audio_processing.main(file.filename, AUDIO_FOLDER)
        return jsonify({'success': 'File uploaded successfully', 'file_path': file_path})

if __name__ == '__main__':
    app.run(port=3000, debug=True)


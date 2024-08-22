import os
import io
from flask import Flask, render_template, request, flash, redirect, jsonify, make_response, send_file, session, url_for
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
from utils import *

app = Flask(__name__, template_folder='templates/')
app.secret_key = 'BAD_SECRET_KEY'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'audio')
STYLE_FOLDER = os.path.join(BASE_DIR, 'style')
FONT_FOLDER = os.path.join(BASE_DIR, 'fonts')
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

app.config['DATA_FOLDER'] = DATA_FOLDER

# Ensure CSV files exist
if not os.path.exists(USERS_CSV):
    with open(USERS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username'])

if not os.path.exists(RECORDINGS_CSV):
    with open(RECORDINGS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'filename', 'timestamp'])

# Route for the home page
@app.route('/')
def index():
    # if 'logged_in' in session and session['logged_in']:
    #     return render_template('index.html', username=session['username'])
    # return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # Check if the username already exists
        if user_exists(username):
            flash('Username already exists. Please try again.')
            return redirect(url_for('register'))
        with open(USERS_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username])
        session['logged_in'] = True
        session['username'] = username
        session['filenames'] = []  # Initialize filenames list
        return redirect(url_for('index'))
    return render_template('register.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if user_exists(username):
            session['logged_in'] = True
            session['username'] = username
            session['filenames'] = []  # Initialize filenames list
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('filenames', None)
    # session.clear()
    return redirect(url_for('index'))

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

@app.route('/style/<path:subpath>', methods=['GET'])
def get_style(subpath=''):
    return send_file(os.path.join(STYLE_FOLDER, subpath))

@app.route('/fonts/<path:subpath>', methods=['GET'])
def get_fonts(subpath=''):
    return send_file(os.path.join(FONT_FOLDER, subpath))

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
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'audio' not in request.files:
            app.logger.error('No file part')
            return jsonify({'error': 'No file part'})
        file = request.files['audio']
        if file.filename == '':
            app.logger.error('No selected file')
            return jsonify({'error': 'No selected file'})
        if file:
            filename = file.filename
            file_path = os.path.join(AUDIO_FOLDER, filename) # save to AUDIO_FOLDER
            file.save(file_path)
            file.close()

            # Save filename to session and CSV
            session['filenames'].append(filename)
            with open(RECORDINGS_CSV, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([session['username'], filename])

            app.logger.info(f'File saved to {file_path}')
            # audio_processing.main(file.filename, AUDIO_FOLDER)
            return jsonify({'success': 'File uploaded successfully', 'file_path': file_path})

if __name__ == '__main__':
    app.run(port=3000, debug=True)


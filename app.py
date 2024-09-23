import os
import io
from flask import Flask, render_template, request, flash, redirect, jsonify, make_response, send_file, session, url_for
from flask_cors import CORS
# from werkzeug.utils import secure_filename
# import subprocess
# import sys
# import time
# import pandas as pd
import csv
# import json
import logging
logging.basicConfig(level=logging.DEBUG)
import audio_processing

app = Flask(__name__, template_folder='templates/')
app.secret_key = 'BAD_SECRET_KEY'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'audio')
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
USERS_CSV = os.path.join(DATA_FOLDER, 'users.csv')
RECORDINGS_CSV = os.path.join(DATA_FOLDER, 'recordings.csv')
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

app.config['DATA_FOLDER'] = DATA_FOLDER

# Checks so file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to check if user exists
def user_exists(username):
    with open(USERS_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return True
    return False

# Ensure CSV files exist
if not os.path.exists(USERS_CSV):
    with open(USERS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username'])

if not os.path.exists(RECORDINGS_CSV):
    with open(RECORDINGS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'filename', 'timestamp'])

DEV_MODE = False

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/record')
def recorder():
    if(DEV_MODE):
        session['logged_in'] = True
        session['username'] = 'admin'
    if 'logged_in' in session and session['logged_in']:
        app.logger.info(f'Current username: { session["username"] }')
        return render_template('recorder.html', username=session['username'])
    else:
        return redirect(url_for('index'))
    #     session['filenames'] = []
    # if 'logged_in' not in session or not session['logged_in']:
    #     return redirect(url_for('login'))
    # else:
    #     app.logger.info(f'Current username: { session["username"] }') #更改了这一行的缩进和单引号变双引号之后可以跑了
    # return render_template('recorder.html', username=session['username'])
    
        
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
        # session['logged_in'] = True
        # session['username'] = username
        # session['filenames'] = []  # Initialize filenames list
        return redirect(url_for('login'))
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
            return redirect(url_for('recorder'))
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

# icon
@app.route('/favicon.ico')
def favicon():
    return send_file(os.path.join(BASE_DIR, 'favicon.ico'))

@app.route('/loading', methods=['GET', 'POST'])
def loading_page():
    return render_template('loading.html') # or change it to loading_jy.html

@app.route('/remix', methods=['GET', 'POST'])
def visualize():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('index')) # todo: pop up a warning for logging in
    username = session['username']

    # if request.form['display_mode'] == 'all'
    data2d_df = audio_processing.embed_data(DATA_FOLDER, export=False)
    # visualize the whole dataset in comparison to the user's sounds
    data2d = data2d_df.to_dict('records') # list of dictionaries
    # visualize the user's sounds
    # if request.form['display_mode'] == 'user'
    # data2d_df = audio_processing.embed_data(DATA_FOLDER, user=username, export=False) # re-calculate embedding
    # data2d = data2d_df[data2d_df['username'] == username].to_dict('records') # the same embedding but partial display
    
    return render_template('audio_viz.html', username=username, feed_data=data2d)

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
            user_dir = os.path.join(AUDIO_FOLDER, session['username'])
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            filename = file.filename
            file_path = os.path.join(user_dir, filename) # save to AUDIO_FOLDER
            file.save(file_path)
            file.close()

            ## feature extraction for each upload
            audio_processing.process(session['username'], filename, AUDIO_FOLDER, DATA_FOLDER)

            # Save filename to session and CSV
            session['filenames'].append(filename)
            with open(RECORDINGS_CSV, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([session['username'], filename])

            app.logger.info(f'File saved to {file_path}')
            # audio_processing.main(file.filename, AUDIO_FOLDER)
            return jsonify({'success': 'File uploaded successfully', 'file_path': file_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)


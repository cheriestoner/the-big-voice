import audio_processing
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'audio')

audio_processing.main("test4.wav", AUDIO_FOLDER, DATA_FOLDER)
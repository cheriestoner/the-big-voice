import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import pandas as pd
import os
from pydub import AudioSegment

CHUNK_SIZE = 500 # millisecond
HOPPING = 1 # 100% hopping, 0 overlapping. for feature extraction

# add your code below
def extractSpectralCentroid(samples, sample_rate, frame_size, hop_size):
    import math
    frame_size = int(frame_size*sample_rate*1e-3) #convert from ms to number of samples
    hop_size = int(hop_size*frame_size) #hop size into number of samples
    frame_number = (len(samples)-frame_size)//hop_size + 1 #number of frames
    spectral_centroids = []
    
    for i in range(frame_number):
        current_frame = samples[i*hop_size: i*hop_size+frame_size]
        N = len(current_frame)
        fft_frame = np.abs(fft(current_frame))[0:((N//2)+1)]
        numerator_factors = []
        for k in range(len(fft_frame)):
            numerator_factors.append((sample_rate*k*fft_frame[k])//N)
            
        numerator = np.sum(numerator_factors)
        denominator = np.sum(fft_frame)
        
        spectral_centroids.append(numerator//denominator)
        

    return spectral_centroids

def RMS(samples, sample_rate, frame_size, hop_size):
    import math
    frame_size = int(frame_size*sample_rate*1e-3) #convert from ms to number of samples
    hop_size = int(hop_size*frame_size) #hop size into number of samples
    frame_number = (len(samples)-frame_size)//hop_size + 1 #number of frames
    rms = []

    for i in range(frame_number):
        current_frame = samples[i*hop_size: i*hop_size+frame_size]
        rms.append(np.sqrt(np.mean(current_frame**2)))
    
    return rms

def normalizeFeature(x):
    x = np.asarray(x)
    x = np.divide(x, np.absolute(x).max())
    return x.tolist()

def save_to_csv(df, file_name, header=True):
    # Check if the file already exists
    if os.path.isfile(file_name):
        # If it exists, append without writing the header
        df.to_csv(file_name, mode='a', header=False, index=False)
    else:
        # If it does not exist, create the file with the header
        df.to_csv(file_name, mode='w', header=header, index=False)


##################################################################
# def main():
    # indent and include below
    # todo: session

# Importing the audiofile
filename = "test_office.wav"
filename_text = filename.rsplit('.', 1)[0].lower() # or file[:-3]
filename_extension = filename.rsplit('.', 1)[1].lower() # or filename[-3:]
# convert file if not .wav
if filename_extension == "mp3":
    wav_audio = AudioSegment.from_mp3(filename)
    filename = filename_text + ".wav"
    wav_audio.export(filename, format="wav")

sound = AudioSegment.from_file(filename, format="wav")
sound = sound.split_to_mono()[0]
#Getting sample rate and samples
sample_rate = sound.frame_rate
duration = sound.duration_seconds
samples = np.divide(sound.get_array_of_samples(), sound.max_possible_amplitude)

num_frames = int(np.ceil(len(samples)/(CHUNK_SIZE*sample_rate*1e-3)))
spectral_centroids = extractSpectralCentroid(samples, sample_rate, CHUNK_SIZE, HOPPING)
rms = RMS(samples, sample_rate, CHUNK_SIZE, HOPPING)

spectral_centroids = normalizeFeature(spectral_centroids)
rms = normalizeFeature(rms)

# Save extracted features to dataframe
# [filename, chunk number (file sub index), start time, end time, spec centroid, rms]

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# data_dir = os.path.join(BASE_DIR, 'data')

data_dir = 'data'
data_file = 'data.csv'
data_file = os.path.join(data_dir, data_file)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

data = []
xyz = []
# for the same audio file
for i in range(num_frames):
    data.append([filename, i, i*CHUNK_SIZE*1e-3, (i+1)*CHUNK_SIZE*1e-3, spectral_centroids[i], rms[i]])
    xyz.append([spectral_centroids[i], rms[i], 0])

data_df = pd.DataFrame(data, columns = ['filename', 'chunk index', 'start time sec', 'end time sec', 'centroid', 'rms'])
xyz_df = pd.DataFrame(xyz)

save_to_csv(data_df, data_file)
save_to_csv(xyz_df, 'data/xyz.csv', header=False)

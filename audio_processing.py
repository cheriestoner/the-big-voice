import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import pandas as pd
import os
from pydub import AudioSegment

CHUNK_SIZE = 500 # millisecond
HOPPING = 1 # 100% hopping, 0 overlapping. for feature extraction

def calculate_frame_num(num_sample, sample_rate, frame_size, hopping):
    frame_size = int(frame_size * sample_rate * 1e-3)
    hop_size = int(hopping * frame_size)
    return int(np.ceil(num_sample-frame_size)/hop_size) + 1

# add your code below
def extractSpectralCentroid(samples, sample_rate, frame_size, hop_size):
    '''
    samples: audio in samples
    sample_rate: sample rate, normally 48000
    frame_size: frame size in millisecond
    hop_size: percentage of frame size
    '''
    frame_size = int(frame_size*sample_rate*1e-3) # convert from ms to number of samples
    hop_size = int(hop_size*frame_size) # hop size into number of samples
    frame_number = int(np.ceil((len(samples)-frame_size)/hop_size) + 1) #number of frames
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

def extractRMS(samples, sample_rate, frame_size, hop_size):
    '''
    samples: audio in samples
    sample_rate: sample rate, normally 48000
    frame_size: frame size in millisecond
    hop_size: percentage of frame size
    '''
    frame_size = int(frame_size*sample_rate*1e-3) #convert from ms to number of samples
    hop_size = int(hop_size*frame_size) #hop size into number of samples
    frame_number = int(np.ceil((len(samples)-frame_size)/hop_size) + 1) #number of frames
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
def main(audiofile="test_office.wav", audio_folder='audio'):
    # Importing the audiofile
    # audiofile = "test_office.wav"
    audiofile_text = audiofile.rsplit('.', 1)[0].lower() # or file[:-3]
    audiofile_extension = audiofile.rsplit('.', 1)[1].lower() # or audiofile[-3:]
    # convert file if not .wav
    if audiofile_extension == "mp3":
        wav_audio = AudioSegment.from_mp3(audiofile)
        audiofile = audiofile_text + ".wav"
        wav_audio.export(audiofile, format="wav")

    # print('processing file: ', os.path.join(audio_folder, audiofile))
    sound = AudioSegment.from_file(os.path.join(audio_folder, audiofile)) # , format="wav") does not work for werkzeug file?
    sound = sound.split_to_mono()[0]
    #Getting sample rate and samples
    sample_rate = sound.frame_rate
    duration = sound.duration_seconds
    samples = np.divide(sound.get_array_of_samples(), sound.max_possible_amplitude)

    spectral_centroids = extractSpectralCentroid(samples, sample_rate, CHUNK_SIZE, HOPPING)
    rms = extractRMS(samples, sample_rate, CHUNK_SIZE, HOPPING)

    spectral_centroids = normalizeFeature(spectral_centroids)
    rms = normalizeFeature(rms)

    # Save extracted features to dataframe
    # [audiofile, chunk number (file sub index), start time, end time, spec centroid, rms]

    data_dir = os.path.join('data', audiofile_text)
    data_file = 'data.csv'
    data_file = os.path.join(data_dir, data_file)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data = []
    # for the same audio file
    num_chunks = calculate_frame_num(len(samples), sample_rate, CHUNK_SIZE, HOPPING)
    for i in range(num_chunks):
        data.append([audiofile, i, i*CHUNK_SIZE*1e-3, (i+1)*CHUNK_SIZE*1e-3, spectral_centroids[i], rms[i]])

    data_df = pd.DataFrame(data, columns = ['audiofile', 'chunk index', 'start time sec', 'end time sec', 'centroid', 'rms'])

    save_to_csv(data_df, data_file)

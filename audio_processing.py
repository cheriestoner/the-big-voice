import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import pandas as pd
import os
from pydub import AudioSegment
import librosa
# from umap import UMAP

SEGMENT_SIZE = 500 # millisecond
HOPPING = 1 # 100% hopping, 0 overlapping. for feature extraction

def load_audio_pydub(filepath):
    file_text = filepath.rsplit('.', 1)[0].lower() # or file[:-3]
    file_extension = filepath.rsplit('.', 1)[1].lower() # or audiofile[-3:]
    if file_extension == "mp3":
        wav_audio = AudioSegment.from_mp3(filepath)
        filepath = file_text + "wav" # set new audio_path
        wav_audio.export(filepath, format="wav")
    sound = AudioSegment.from_file(filepath) #, format='wav')
    sound = sound.split_to_mono()[0]
    # Getting sample rate and samples
    sample_rate = sound.frame_rate
    duration = sound.duration_seconds
    sound_arr = np.divide(sound.get_array_of_samples(), sound.max_possible_amplitude)
    return sound_arr, sample_rate, duration

def calculate_frame_num(num_sample, sr, frame_size, hopping):
    frame_size = int(frame_size * sr * 1e-3)
    hop_size = int(hopping * frame_size)
    return int(np.ceil(num_sample-frame_size)/hop_size) + 1

# add your code below
def extractSpectralCentroid(samples, sample_rate, frame_size, hop_size):
    '''
    samples: audio in samples
    sample_rate: sample rate, 48000 for iPhone recordings
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
    '''
    x: ndarray
    '''
    # x = np.asarray(x)
    x = np.divide(x, np.absolute(x).max())
    return x.tolist()

def save_data_csv(dataframe, data_dir, data_file='data.csv'):
    # Save raw features dataframe to csv
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    data_file = os.path.join(data_dir, data_file) # <data_dir>/data.csv
    
    dataframe.to_csv(data_file, mode='w', header=True, index=False) # data_file name always unique

def millisec2sample(size, sr=48000):
    return int(size*sr*1e-3)

##################################################################
def process(username='admin', audiofile="test1.wav", audio_folder='audio', data_folder='data'):
    # Importing the audiofile
    # audiofile = "test_office.wav"
    
    sound_arr, sr, duration = load_audio_pydub(os.path.join(audio_folder, username, audiofile))

    # print('processing file: ', os.path.join(audio_folder, audiofile))

    spectral_args = {"n_fft":millisec2sample(SEGMENT_SIZE), 
                     "hop_length":millisec2sample(HOPPING*SEGMENT_SIZE), 
                     "center":False}
    temporal_args = {"frame_length":millisec2sample(SEGMENT_SIZE), 
                     "hop_length":millisec2sample(HOPPING*SEGMENT_SIZE), 
                     "center":False}

    rms = librosa.feature.rms(y=sound_arr, **temporal_args)[0]
    zcr = librosa.feature.zero_crossing_rate(y=sound_arr, **temporal_args)[0]
    sc = librosa.feature.spectral_centroid(y=sound_arr, sr=sr, **spectral_args)[0]
    sf = librosa.feature.spectral_flatness(y=sound_arr, **spectral_args)[0]
    mfccs = librosa.feature.mfcc(y=sound_arr, sr=sr, n_mfcc=20, **spectral_args) # matrix
    mfcc_delta = librosa.feature.delta(mfccs)
    mfcc_delta2 = librosa.feature.delta(mfcc_delta)

    # spectral_centroids = extractSpectralCentroid(sound_arr, sr, SEGMENT_SIZE, HOPPING)
    # rms = extractRMS(sound_arr, sr, SEGMENT_SIZE, HOPPING)
    # spectral_centroids = normalizeFeature(spectral_centroids)
    # rms = normalizeFeature(rms)

    # Save extracted features to dataframe
    # [audiofile, segment number (file sub index), start time, end time, features]
    data = []
    for i in range(sc.shape[-1]): # loop over num segments
        end_time = (i+1)*SEGMENT_SIZE*1e-3
        if end_time >= duration: end_time = duration
        data_i = [i, i*SEGMENT_SIZE*1e-3, end_time, rms[i], zcr[i], sc[i], sf[i]]
        data_i.extend(mfccs.T[i].tolist() + mfcc_delta.T[i].tolist() + mfcc_delta2.T[i].tolist())
        data.append(data_i)

    columns = ['segment_index', 'start_time_sec', 'end_time_sec', 'rms', 'zero_crossing_rate', 'spectral_centroid', 'spectral_flatness']
    # mfcc_columns = [f'mfcc_{j+1}' for j in range(mfccs.shape[0])]
    for j in range(mfccs.shape[0]):
        columns.append(f'mfcc_{j+1}')
    for j in range(mfccs.shape[0]):
        columns.append(f'mfcc_delta_{j+1}')
    for j in range(mfccs.shape[0]):
        columns.append(f'mfcc_delta2_{j+1}')

    data_df = pd.DataFrame(data, columns = columns)
    data_dir = os.path.join(data_folder, username, audiofile.rsplit('.', 1)[0])
    save_data_csv(data_df, data_dir) #/data/<username>/<filename>/data.csv

    # return data_df

def embed_data(data_folder='data'):
    '''
    Reduce dimensionality of the whole dataset of features
    '''
    from sklearn.manifold import TSNE
    recordings = pd.read_csv(os.path.join(data_folder, 'recordings.csv'))#['recording_file'].tolist()
    features = []
    items = []
    for idx in recordings.index: # loop over all recording files
        username = recordings['username'][idx]
        recording = recordings['recording_file'][idx] # with .wav extension
        data_file = os.path.join(data_folder, username, recording.rsplit('.', 1)[0], 'data.csv')
        df = pd.read_csv(data_file, header=0)
        features_i = df.iloc[:, 3:].values
        item = df.iloc[:, 0:3].values
        recording_col = np.array([[recording] for i in range(item.shape[0])])
        username_col = np.array([[username] for i in range(item.shape[0])])
        item = np.concatenate([recording_col, item], axis=1)
        item = np.concatenate([username_col, item], axis=1)
        if (np.size(features) == 0): features = features_i
        else: features = np.append(features, features_i, axis=0) # ndarray (num_seg, 64 feature dimensions)
        if (np.size(items) == 0): items = item
        else: items = np.append(items, item, axis=0)
    # features = np.array(features) # raw features
    # items = np.array(items) # ['username', 'audiofile', 'segment_index', 'start_time_sec', 'end_time_sec']
    # print(features.shape)

    # print(features.shape[0], items.shape[0])
    # umap_2d = UMAP(n_components=2, n_jobs=1, init='random', random_state=0)
    # umap_2d = UMAP(n_jobs=1, metric='cosine', random_state=42, low_memory=True)
    # umap_2d = UMAP(n_jobs=1, metric='hellinger', random_state=42) # only non-negative values
    # features_embedded = umap_2d.fit_transform(features)
    tsne = TSNE(n_components=2, learning_rate='auto', perplexity=30)
    features_embedded = tsne.fit_transform(features)
    # print(features_embedded.shape)
    data_2d = np.append(items, features_embedded, axis=1)
    
    # save 2D coordinates
    filepath = os.path.join(data_folder, 'coords.csv')
    columns = ['username', 'audiofile', 'segment_index', 'start_time_sec', 'end_time_sec', 'embedding_x', 'embedding_y']
    data_df = pd.DataFrame(data_2d, columns = columns)
    data_df.to_csv(filepath, mode='w', header=True, index=False)
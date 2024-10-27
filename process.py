import audio_processing
import pandas as pd
i = 4
# audio_processing.process('agrainof', f"test{i}.wav", 'audio', 'data')
# audio_processing.process('admin', "2024-09-09-17-13-32.wav", 'audio', 'data')

recordings = pd.read_csv('data/recordings.csv')
for idx in recordings.index: # loop over all recording files
    username = recordings['username'][idx]
    recording = recordings['recording_file'][idx] # with .wav extension
    audio_processing.process(username=username, audiofile=recording, audio_folder='audio', data_folder='data')

# audio_processing.embed_data(user='all', embed='tsne', data_folder='data', export=True)
# the-big-voice

Keylab

**Team:** 

Lio (Frontend dev, UI design)

Jiayi (Frontend dev, Fullstack dev)

Xuehua (Fullstack dev, System design)

**To-dos for developers:**

- Cloud deployment /Jiayi
    - Git

- Recorder page: /Jiayi
    - ~Upload audio to server~
    - ~Next button go to remixer /Jiayi~
        - ~call audio_processing.main() on server end/Xuehua~
    - ~User recording filename as a variable & send to remixer /Xuehua~
    - ~Naming user recording with timestamp (inside audio.js) /Lio~
    - ~Upload and store recording data in recordings.csv~
    - ~Improve layout: waveform below the start button, footnote fixed at the bottom~
    - Limit the recording duration
    - LPF and HPF to enhance recording

- Loading page (low priority for now)
    - ~Placeholder animation~
    - Skeleton screen (loading scatterplot)

- Remixer page: /Lio
    - ~mouseOver play audio~
    - ~Recording list~
    - ~Visualize 'data_2d.csv' /Xuehua~
    - ~Play a neighborhood of sounds (mouse cursor with a collision area instead of a dot)~
    - ~Circle selection disappears after 10 sec~
    - ~How to mix an area of sounds: sounds from the current user as foreground, sound from tha dataset as background? Volumn control + reverb?~
    - Different modes for navigating the plot? area selection and single dot play?
    - Loop play?

- Backend management: /Xuehua
    - flask feed list data to html instead of d3.csv()
    - ~flask user session, without authentication, login with username~
    - maintain a CONSTANTS.py?
    - store recording metadata: date, time, location

- Audio processing: /Xuehua
    - dynamic segmentation
    - filter out segments under rms threshold
    - Feature extraction
        - ~MFCC first & second derivatives (delta)~
    - Sound event localization?
    - Dimensionality reduction (SNE/PCA/UMAP)
        - ~Unsupervised T-SNE~
        - T-SNE semi-supervision with user labels?

- UI decorations
    - ~CSS style in separate files /Lio~


---

**Concept**

(briefly write our concept here)

**Main objectives**

1. User record, upload, and remix
2. Specific feature set (for environmental soundscape?)
3. Feature dimensionality reduction (soundscape descriptors?)
4. Cluster
4. Interactive scatterplot
4. GPU rendering

**Possible innovations**

- User annotation/user specified descriptors for the recordings
- Guided user interface: theme/category/hints for users to record certain sounds
- Concatenative visualization playability: area-wise sound composition/design/remix, creative play mode, link to images/locations/other descriptives

**Technical extensions**

- 

---

**Installation instructions**

- Install the latest version of [Python](https://www.python.org/downloads/). Check if it is installed successfully by running `python --version` in Terminal.

- Install ffmpeg and add to path

- Clone the repository on your on laptop.

- In Terminal, go to the project folder. Install package dependencies by running `pip install requirements.txt`.

- Start the app on your local server by running `python app.py` in Terminal, and go to the website via the url.
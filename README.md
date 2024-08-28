# the-big-voice

Keylab

**Team:** 

Lio (Frontend dev, UI design)

Jiayi (Frontend dev, Fullstack dev)

Xuehua (Fullstack dev, System design)

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

- Clone the repository on your on laptop.

- In Terminal, go to the project folder. Install package dependencies by running `pip install requirements.txt`.

- Start the app on your local server by running `python app.py` in Terminal, and go to the website via the url.

---

**To-dos for developers:**

- Recorder page: /Jiayi
    - ~Upload audio to server~
    - ~Next button go to remixer /Jiayi~
        - ~call audio_processing.main() on server end/Xuehua~
    - ~User recording filename as a variable & send to remixer /Xuehua~
    - ~Naming user recording with timestamp (inside audio.js) /Lio~
    - Limit the recording duration

- Loading page (low priority for now)
    - ~Placeholder animation~
    - Skeleton screen (loading scatterplot)

- Remixer page: /Lio
    - ~mouseOver play audio~
    - ~Button to go back to recorder~
    - ~Plot a list of .csv files on one graph~
    - ~color highlight user recording?~
    - ~One button~
    - ~Recording list~

- Backend management: /Xuehua
    - flask feed list data to html instead of d3.csv()
    - maintain a global value range (variable) for each feature, calculated from the current dataset
    - ~flask user session, without authentication, login with username~
    - maintain a CONSTANTS.py?
    - store recording metadata: date, time, location

- Audio processing: /Xuehua
    - Feature extraction
    - Dimensionality reduction (SNE or PCA)

- UI decorations
    - ~CSS style in separate files /Lio~

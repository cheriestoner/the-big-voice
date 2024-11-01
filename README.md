# Keylab - The Big Voice

**Team:** 

Lio (Frontend dev)

Jiayi (Fullstack dev)

Xuehua (Fullstack dev, System design)

Hao (UI design, Frontend dev)

---

## For developers:

### TODOs for the next days:
Hao:
- Design the user registration webpage
- Redesign the recorder page with LPF and HPF functionalities

Lio:
- Fix the bug with audio replaying on iPhones
- LPF and HPF functionalities for the recorder
- Reduce loop play duration from 10 seconds to 3-5 seconds on the remixer page

Xuehua:
- Optimize the data pipeline
- Optimze database with SQL? (or is Jiayi interested in trying this?)
- Fix audio replay lagging: Preload audio files on the HTML?
- Redesign the remixer (sound browser) UI with Hao

Jiayi:
- (Optimze database with SQL?)

### Tasks

#### Frontend functionalities:
- Recorder page:
    - ~Limit the recording duration~
    - LPF and HPF to enhance recording
- Remixer page:
    - ~Area play mode, loop play (10 seconds)~
    - Customize colors
      
#### UI design / Hao
- Webpage for user account registration
- **Recorder page:**
    - allow the user to apply low-pass filter, high-pass filter, or none and choose one result to upload
- Loading page (low priority): Skeleton screen (loading scatterplot)

#### Backend management:
- File storage
    - store recording metadata: date, time, location
- Audio processing: /Xuehua
    - dynamic segmentation
    - filter out segments under rms threshold
    - Feature extraction
        - ~MFCC first & second derivatives (delta)~ (`mfcc_delta` default width = 9 frames)
    - Dimensionality reduction (t-SNE/PCA/UMAP)
        - ~Unsupervised t-SNE & UMAP~
        - Semi-supervision with user specified class labels/tags?
- Cloud deployment /Jiayi

### Installation instructions

- Install ffmpeg and add to path

- Install Miniconda and add to path

- Clone the repository

- Use conda to create an virtual environment: `conda env create -f environment.yml`

- Activate the environment by `source activate the-big-voice` or `conda activate the-big-voice`

- Run the flask app in the environment by `(the-big-voice) $ python app.py`

- Start the app on your local server by running `python app.py` in Terminal, and visit the site via the IP address.

### Remote console on Huawei Cloud

On Huawei Cloud, go to console and then

1. Activate virtual environment by `conda acitvate the-big-voice`

2. Go to the project folder: `cd /www/wwwroot/the-big-voice`

3. Run Flask app in the background using `nohup`: `nohup python app.py &`

4. Check status of the app using `tail`: e.g. `tail -n 20 nohup.out` shows the last 20 lines of the log
    
5. How to kill the process
    - Get the process ID by
    `ps aux | grep python`
    - Kill the process by ID
    `kill <PID>`

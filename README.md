# the-big-voice

Keylab

**Team:** 

Lio (Frontend dev)

Jiayi (Fullstack dev)

Xuehua (Fullstack dev, System design)

Hao (UI design, Frontend dev)

**Cloud server usage:**

On Huawei Cloud:

1. Activate virtual environment

    `conda acitvate the-big-voice`

2. Go to the project folder

    `cd /www/wwwroot/the-big-voice`

3. Run Flask app in the background using `nohup`

    `nohup python app.py &`

4. Check status of the app

    `tail -n 20 nohup.out` shows the last 20 lines of the log
    
5. How to kill the process
    - Find the process ID by
    `ps aux | grep python`
    - Kill the process by ID
    `kill <PID>`

**To-dos for developers:**

- Cloud deployment /Jiayi
    - Git

- Recorder page: /Jiayi
    - Limit the recording duration
    - LPF and HPF to enhance recording

- Loading page (low priority)
    - Skeleton screen (loading scatterplot)

- Remixer page: /Lio
    - ~Area play mode~
    - ~Loop play (10 seconds)~
    - 

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
        - the recording has to be at least 0.5*9=4.5s. (Each recording is sliced into 0.5s frames, mfcc_delta default width is 9 frames.)
    - Sound event localization?
    - Dimensionality reduction (SNE/PCA/UMAP)
        - ~Unsupervised T-SNE~
        - ~Unsupervised UMAP~
        - Semi-supervision with user specified labels? (but labels are only )

- UI decorations
    - ~CSS style in separate files /Lio~

---

**Installation instructions**

- Install ffmpeg and add to path

- Install Miniconda

- Clone the repository on your on laptop via Git

- Use conda to create an virtual environment:

    `conda env create -f environment.yml`

- Activate the environment

    `source activate the-big-voice`

- Run the flask app in the environment:

    `(the-big-voice) $ python app.py`

- Start the app on your local server by running `python app.py` in Terminal, and go to the website via the url.
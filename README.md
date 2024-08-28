# the-big-voice
Keylab

**Team:** 
Lio (Frontend dev, UI design)

Jiayi (Frontend dev, Fullstack dev)

Xuehua (Fullstack dev, System design)

**Main objectives**
1. User record, upload, and remix
2. Specific feature set (for environmental soundscape?)
3. Feature dimensionality reduction (soundscape descriptors?)
4. Cluster
4. Interactive scatterplot: play audio with mouse on
4. GPU rendering

**To-do functionalities:**
- Index page: /Jiayi
    - ~Upload audio to server~
    - ~Next button go to remixer /Jiayi~
        - ~call audio_processing.main() on server end/Xuehua~
    - ~User recording filename as a variable & send to remixer /Xuehua~
    - ~Naming user recording with timestamp (inside audio.js) /Lio~
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
- UI decorations
    - ~CSS style in separate files /Lio~

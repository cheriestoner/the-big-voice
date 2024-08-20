# the-big-voice
Keylab

**Team:** 
Lio (Frontend dev, UI design)

Jiayi (Frontend dev, Fullstack dev)

Xuehua (Fullstack dev, System design)

**To-do functionalities:**
- Index page: /Jiayi
    - ~上传音频到服务器~
    - ~Next button 跳转到remixer /Jiayi~
        - ~后台调用audio_processing.main() /Xuehua~
    - ~User录音文件命名用variable存储 & 传给remixer /Xuehua~
    - User recording 命名带timestamp
- Loading page (暂时不需要)
    - ~Placeholder animation~
    - Skeleton screen (loading scatterplot)
- Remixer page: /Lio
    - ~mouseOver play audio~
    - ~Button to go back to recorder~
    - Plot 2 .csv files on one graph
- Backend management: /Xuehua
    - flask feed list data to html instead of d3.csv()
    - maintain a global value range (variable) for each feature, calculated from the current dataset
    - "user session" color highlight user recording?
    - maintain a CONSTANTS.py?
    - store recording metadata: time, location

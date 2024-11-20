const loginButton = document.getElementById('loginButton');
const recordButton = document.getElementById('recordButton');
const recordButtonImg = recordButton.querySelector('img');
const stopButton = document.getElementById('stopButton');
const recordingsList = document.getElementById('recordingsList');
const recordingTimer = document.getElementById('recordingTimer');

let mediaRecorder;
let audioChunks = [];
let audioBlob;
let audioContext;
let analyser;
let dataArray;
let canvas;
let canvasCtx;
let drawVisual;
let isRecording = false;
let fileName;
let minRecordTime = 5000;
let maxRecordTime = 30000;
let recordTimeout;
let startTime;
let viewWidth = window.innerWidth;
let viewHeight = window.innerHeight;
let visualTime;
let timerInterval;

// 实时录制时间,格式mm:ss.ms
function formatTime(duration) {
    const milliseconds = Math.floor((duration % 1000) / 10);
    const seconds = Math.floor((duration / 1000) % 60);
    const minutes = Math.floor((duration / (1000 * 60)) % 60);

    const formattedMinutes = minutes.toString().padStart(2, '0');
    const formattedSeconds = seconds.toString().padStart(2, '0');
    const formattedMilliseconds = milliseconds.toString().padStart(2, '0');

    return `${formattedMinutes}:${formattedSeconds}.${formattedMilliseconds}`;
}

// 开始timer
function startRecordingTimer() {
    visualTime = Date.now();
    recordingTimer.style.display = 'block'; 
    recordingTimer.style.position = 'absolute';  
    recordingTimer.style.bottom = '10px'; 
    recordingTimer.style.right = '10px';  
    timerInterval = setInterval(() => {
        const elapsedTime = Date.now() - visualTime;
        recordingTimer.textContent = formatTime(elapsedTime);
    }, 10); // 每10ms更新时间
}

// 停止timer
function stopRecordingTimer() {
    clearInterval(timerInterval);
    recordingTimer.textContent = '00:00.00'; // 重置timer
    recordingTimer.style.display = 'none'; // 隐藏
}

// debug recordButton
function updateRecordButtonState() {
    isRecording = !isRecording;
    if (isRecording) {
        recordButtonImg.src = recordButtonImg.getAttribute('data-on-src');
    } else {
        recordButtonImg.src = recordButtonImg.getAttribute('data-off-src');
    }
    console.log(`Record button updated: isRecording = ${isRecording}`);
}


recordButton.addEventListener('click', async (event) => {
    event.stopPropagation();
    console.log("Button clicked");
    if (!isRecording) {
        // 开始录制
        updateRecordButtonState();
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        // 创建timer
        const visualContainer = document.createElement('div');
        visualContainer.style.position = 'relative'; 
        visualContainer.style.width = '100%';
        visualContainer.style.height = '520px';  // Increased height to include both canvas and timer
        visualContainer.style.margin = '150px 0 0';
        document.body.appendChild(visualContainer);

        // 获取Canvas元素和上下文
        canvas = document.createElement('canvas');
        // 将Canvas插入到article元素之后
        // const article = document.querySelector('body');
        // article.appendChild(canvas);
        visualContainer.appendChild(canvas);
        // const audio = document.querySelector('audio');
        // audio.insertAdjacentElement('beforebegin', canvas);
        canvasCtx = canvas.getContext('2d');
        canvas.width = viewWidth;
        canvas.height = viewHeight * 0.3;
        canvas.style.margin = '150px 0 0';

        // 将计时器移入容器并置于canvas下方
        recordingTimer.style.position = 'absolute';
        recordingTimer.style.bottom = '10px';
        recordingTimer.style.right = '10px';
        visualContainer.appendChild(recordingTimer);

        // 显示和启动timer
        startRecordingTimer(); 
        mediaRecorder.start();
        // isRecording = true;

        recordButton.disabled = true;
        setTimeout(() => {
            recordButton.disabled = false; // Enable the button after 5 seconds
            console.log("You can now stop the recording.");
        }, minRecordTime);

        startTime = Date.now();
        recordTimeout = setTimeout(() => {
            mediaRecorder.stop(); // 超过60秒停止录制
            stopRecordingTimer(); 
            updateRecordButtonState();
        }, maxRecordTime);

        // 初始化音频上下文和分析节点
        audioContext = new AudioContext();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 2048;
        const bufferLength = analyser.fftSize;
        dataArray = new Uint8Array(bufferLength);

        // 在用户交互后恢复 AudioContext
        function resumeAudioContext() {
            if (audioContext.state === 'suspended') {
                audioContext.resume().then(() => {
                    console.log('AudioContext resumed.');
                });
            }
        }

        // 在用户首次交互时恢复 AudioContext
        document.body.addEventListener('click', resumeAudioContext, { once: true });

        source.connect(analyser);
    
        function draw() {
            drawVisual = requestAnimationFrame(draw);
            analyser.getByteTimeDomainData(dataArray);
        
            canvasCtx.fillStyle = 'rgb(219, 235, 200)';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
        
            canvasCtx.lineWidth = 3;
            canvasCtx.strokeStyle = 'rgb(125, 118, 101)';
        
            canvasCtx.beginPath();
            const sliceWidth = canvas.width * 1.0 / bufferLength;
            let x = 0;
        
            for (let i = 0; i < bufferLength; i++) {
                const v = dataArray[i] / 128.0;
                const y = v * canvas.height / 2;
            
                if (i === 0) {
                    canvasCtx.moveTo(x, y);
                } else {
                    canvasCtx.lineTo(x, y);
                }
            
                x += sliceWidth;
            }
        
            canvasCtx.lineTo(canvas.width, canvas.height / 2);
            canvasCtx.stroke();
        }
    
        draw();

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
    
        mediaRecorder.onstop = () => {
            const currentAudioBlob = new Blob(audioChunks, { type: 'audio/mp4' });
            const audioUrl = URL.createObjectURL(currentAudioBlob);
            audioChunks = [];
            // 停止绘图，移除Canvas
            cancelAnimationFrame(drawVisual);
            // canvas.remove();
            visualContainer.remove();

            function addTimeToFileName(originalFileName) {
                const now = new Date();
                const year = now.getFullYear();
                const month = (now.getMonth() + 1).toString().padStart(2, '0');
                const day = now.getDate().toString().padStart(2, '0');
                const hours = now.getHours().toString().padStart(2, '0');
                const minutes = now.getMinutes().toString().padStart(2, '0');
                const seconds = now.getSeconds().toString().padStart(2, '0');
               
                const dateTimeString = `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`;
                // return `${originalFileName}_${dateTimeString}${'.wav'}`;
                // return `${dateTimeString}${'.wav'}`;
                return `${dateTimeString}${'.mp4'}`;
            }
            
            const currentFileName = addTimeToFileName(''); //recording_2024-08-21-14-35-45.wav

            // 创建录音列表 create recording list
            const listItem = document.createElement('div');
            listItem.classList.add('recording-item');
            // 创建删除键 create delete button
            const deleteButton = document.createElement('button');
            // deleteButton.textContent = 'Delete';
            // deleteButton.id = 'delete-button';
            deleteButton.classList.add('delete-button');
            deleteButton.addEventListener('click', () => {
                recordingsList.removeChild(listItem);
            });
            // 创建上传键 create upload button
            const submitButton = document.createElement('button');
            // submitButton.textContent = 'Upload';
            // submitButton.id = 'submit-button';
            submitButton.classList.add('upload-button'); 

            submitButton.addEventListener('click', () => {
                if (currentAudioBlob) {
                    const formData = new FormData();
                    formData.append('audio', currentAudioBlob, currentFileName);
            
                    fetch('/upload-audio', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Upload Success:', data);
                        // submitButton.textContent = 'Done!';
                        submitButton.classList.add('sumbitDone');
                        submitButton.disabled = true;
                    })
                    .catch(error => {
                        console.error('Upload Fail:', error);
                    });
                } else {
                    console.log('No Available Recording!');
                }
            });
            // 创建音频播放按钮
            const audioElement = document.createElement('audio');
            audioElement.id = 'audioPlayback';
            audioElement.controls = true;
            audioElement.src = audioUrl;
            // 创建音频文件名
            const fileNameElement = document.createElement('span');
            fileNameElement.textContent = currentFileName;
            
            listItem.appendChild(fileNameElement);
            listItem.appendChild(deleteButton);
            listItem.appendChild(submitButton);
            listItem.appendChild(audioElement);
            recordingsList.appendChild(listItem);

            // 重置fileName
            fileName = addTimeToFileName('recording');
        };

    } else {
        mediaRecorder.stop();
        updateRecordButtonState();
    }
});

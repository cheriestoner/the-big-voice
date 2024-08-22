const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const recordingsList = document.getElementById('recordingsList');
const nextButton = document.getElementById('gotoRemixer');

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

recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        // 开始录制
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        // 初始化音频上下文和分析节点
        audioContext = new AudioContext();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 2048;
        const bufferLength = analyser.fftSize;
        dataArray = new Uint8Array(bufferLength);

        source.connect(analyser);
    
        // 获取Canvas元素和上下文
        canvas = document.createElement('canvas');
        // 将Canvas插入到article元素之后
        const article = document.querySelector('body');
        article.appendChild(canvas);
        // const audio = document.querySelector('audio');
        // audio.insertAdjacentElement('beforebegin', canvas);
        canvasCtx = canvas.getContext('2d');
        canvas.width = 800;
        canvas.height = 100;
    
        function draw() {
            drawVisual = requestAnimationFrame(draw);
            analyser.getByteTimeDomainData(dataArray);
        
            canvasCtx.fillStyle = 'rgb(230, 228, 215)';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
        
            canvasCtx.lineWidth = 2;
            canvasCtx.strokeStyle = 'rgb(58, 171, 81)';
        
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
            audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioChunks = [];
            
            cancelAnimationFrame(drawVisual); // 停止绘图
            canvas.remove(); // 移除Canvas

            function addTimeToFileName(originalFileName) {
                const now = new Date();
                const year = now.getFullYear();
                const month = (now.getMonth() + 1).toString().padStart(2, '0');
                const day = now.getDate().toString().padStart(2, '0');
                const hours = now.getHours().toString().padStart(2, '0');
                const minutes = now.getMinutes().toString().padStart(2, '0');
                const seconds = now.getSeconds().toString().padStart(2, '0');
               
                const dateTimeString = `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`;
                return `${originalFileName}_${dateTimeString}${'.wav'}`;
            }

            // 创建录音列表
            const listItem = document.createElement('div');
            listItem.classList.add('recording-item');
            // 创建删除键
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.id = 'deleteButton';
            deleteButton.addEventListener('click', () => {
                recordingsList.removeChild(listItem);
            });
            // 创建上传键
            const submitButton = document.createElement('button');
            submitButton.textContent = 'Upload';
            submitButton.id = 'submitButton';

            submitButton.addEventListener('click', () => {
                if (audioBlob) {
                    const formData = new FormData();
                    formData.append('audio', audioBlob, fileName);
            
                    fetch('http://127.0.0.1:3000/upload-audio', {  // 更改为服务器的实际上传地址
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Upload Success:', data);
                        submitButton.textContent = 'Done!';
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
            fileName = addTimeToFileName('recording'); //recording_2024-08-21-14-35-45.wav
            const fileNameElement = document.createElement('span');
            fileNameElement.textContent = fileName;
            
            listItem.appendChild(fileNameElement);
            listItem.appendChild(deleteButton);
            listItem.appendChild(submitButton);
            listItem.appendChild(audioElement);
            recordingsList.appendChild(listItem);
        };
        
        mediaRecorder.start();
        isRecording = true;
        recordButton.id = 'stopButton';
        recordButton.textContent = 'Stop';

    } else {
        // 停止录制
        mediaRecorder.stop();
        isRecording = false;
        recordButton.id = 'recordButton';
        recordButton.textContent = 'Start';
    }
});

nextButton.addEventListener('click', () => {
    window.location.href='/loading/' + fileName; // uncomment it to use the loading page
    // window.location.href='/remix/' + fileName; // comment it to use the loading page
});

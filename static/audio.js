const startButton = document.getElementById('startRecording');
const stopButton = document.getElementById('stopRecording');
const audioPlayback = document.getElementById('audioPlayback');
const submitButton = document.getElementById('submitRecording');

let mediaRecorder;
let audioChunks = [];
let audioBlob;
let audioContext;
let analyser;
let dataArray;
let canvas;
let canvasCtx;
let drawVisual;

startButton.addEventListener('click', async () => {
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
    document.body.appendChild(canvas);
    canvasCtx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 200;

    function draw() {
        drawVisual = requestAnimationFrame(draw);
        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = 'rgb(200, 200, 200)';
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

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
        audioPlayback.src = audioUrl;
        audioChunks = [];
        
        cancelAnimationFrame(drawVisual); // 停止绘图
        canvas.remove(); // 移除Canvas
    };

    mediaRecorder.start();
    startButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
});

submitButton.addEventListener('click', () => {
    if (audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        fetch('http://127.0.0.1:3000/upload-audio', {  // 更改为服务器的实际上传地址
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('上传成功:', data);
        })
        .catch(error => {
            console.error('上传失败:', error);
        });
    } else {
        console.log('没有可上传的录音');
    }
});

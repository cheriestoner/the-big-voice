// 引入 Tone.js 库
import * as Tone from 'https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.28/Tone.js';

const canvas = document.getElementById('mouseCanvas');
const ctx = canvas.getContext('2d');
const audioPlayback = document.getElementById('audioPlayback');
const uploadInput = document.getElementById('uploadAudio');

const coordinates = [];

function calculateAverageAmplitude(buffer) {
    const data = buffer.getChannelData(0);
    let sum = 0;
    for (let i = 0; i < data.length; i++) {
        sum += Math.abs(data[i]);
    }
    return sum / data.length;
}

function calculateAveragePitch(buffer) {
    const pitchAnalyzer = new Tone.FFT(1024);
    const data = buffer.getChannelData(0);
    pitchAnalyzer.getValue(data);
    const frequencies = pitchAnalyzer.getValue();
    let maxAmplitude = -Infinity;
    let dominantFrequency = 0;
    for (let i = 0; i < frequencies.length; i++) {
        if (frequencies[i] > maxAmplitude) {
            maxAmplitude = frequencies[i];
            dominantFrequency = i * (Tone.context.sampleRate / 2) / frequencies.length;
        }
    }
    return dominantFrequency;
}

uploadInput.addEventListener('change', () => {
    const files = uploadInput.files;
    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = async function(event) {
            const arrayBuffer = event.target.result;
            const buffer = await Tone.context.decodeAudioData(arrayBuffer);

            const avgAmplitude = calculateAverageAmplitude(buffer);
            const avgPitch = calculateAveragePitch(buffer);
            
            const x = avgAmplitude * canvas.width;
            const y = (avgPitch / 1000) * canvas.height;

            coordinates.push({ x, y, file });
            drawPoint(x, y);
        };
        reader.readAsArrayBuffer(file);
    });

    function drawPoint(x, y) {
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI, false);
        ctx.fillStyle = 'blue';
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#003300';
        ctx.stroke();
    }

    canvas.addEventListener('mousemove', (event) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        coordinates.forEach(coord => {
            if (Math.abs(coord.x - mouseX) < 5 && Math.abs(coord.y - mouseY) < 5) {
                audioPlayback.src = URL.createObjectURL(coord.file);
                audioPlayback.play();
            }
        });
    });
});

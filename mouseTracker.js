document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('mouseCanvas');
    const ctx = canvas.getContext('2d');
    const squareSize = 400;
    const canvasSize = canvas.width;

    // 计算正方形的左上角坐标，使其在画布中心
    const squareX = (canvasSize - squareSize) / 2;
    const squareY = (canvasSize - squareSize) / 2;

    // 绘制正方形
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(squareX, squareY, squareSize, squareSize);

    // 添加鼠标移动事件监听器
    canvas.addEventListener('mousemove', function (event) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // 检查鼠标是否在正方形范围内
        if (x >= squareX && x <= squareX + squareSize && y >= squareY && y <= squareY + squareSize) {
            // 清除之前的轨迹
            ctx.clearRect(0, 0, canvasSize, canvasSize);
            // 重新绘制正方形
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(squareX, squareY, squareSize, squareSize);

            // 绘制鼠标轨迹点
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'red';
            ctx.fill();
            ctx.lineWidth = 1;
            ctx.strokeStyle = '#003300';
            ctx.stroke();
        } else {
            // 清除正方形外的鼠标轨迹
            ctx.clearRect(0, 0, canvasSize, canvasSize);
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(squareX, squareY, squareSize, squareSize);
        }
    });
});

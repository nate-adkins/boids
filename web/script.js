const canvas = document.getElementById("swarm-environment");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    const availableWidth = window.innerWidth;
    const availableHeight = window.innerHeight - 100;
    const size = Math.min(availableWidth, availableHeight);

    canvas.width = size;
    canvas.height = size;

    canvas.style.width = `${size}px`;
    canvas.style.height = `${size}px`;
}

function drawBoid(ctx, x, y, theta) {
    const heading = theta // -theta - Math.PI/2; // make 0 degrees up, convert to radians 
    const size = 15
    const halfWidth = size / 2;

    const tip_x = x + size * Math.cos(heading);
    const tip_y = y + size * Math.sin(heading);

    const left_x = x + halfWidth * Math.cos(heading + Math.PI * 0.75);
    const left_y = y + halfWidth * Math.sin(heading + Math.PI * 0.75);

    const right_x = x + halfWidth * Math.cos(heading - Math.PI * 0.75);
    const right_y = y + halfWidth * Math.sin(heading - Math.PI * 0.75);

    ctx.beginPath();
    ctx.moveTo(tip_x, tip_y);
    ctx.lineTo(left_x, left_y);
    ctx.lineTo(right_x, right_y);
    ctx.closePath();

    ctx.fillStyle = "#777777";
    ctx.fill();
    ctx.strokeStyle = "#000";
    ctx.lineWidth = size/10;
    ctx.stroke();
}



resizeCanvas();
window.addEventListener('resize', resizeCanvas);
const ws = new WebSocket(`ws://localhost:8765`);
ws.onmessage = (event) => {
    const agents = JSON.parse(event.data);
    console.log
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#777777";
    agents.forEach(a => {
    const x = a.x * canvas.width;
    const y = a.y * canvas.height;
    drawBoid(ctx,x,y,a.theta)
    });
};

const resetBtn = document.getElementById("reset-btn");
resetBtn.addEventListener("click", () => {
    ws.send("reset");  // Send reset command to server
});

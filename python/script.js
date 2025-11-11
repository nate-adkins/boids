const ws = new WebSocket("ws://localhost:8765");

const canvas_padding = 10;
const controls_width = 150;

const canvas = document.getElementById("sim-canvas");
const ctx = canvas.getContext("2d");

const k_param = document.getElementById("k_param")
const s_param = document.getElementById("s_param")
const a_param = document.getElementById("a_param")
const c_param = document.getElementById("c_param")
const reset_btn = document.getElementById("reset-btn")
function drawBoid(theta, x, y) {
    const scaledX = x * canvas.width;
    const scaledY = y * canvas.height;

    const size = 0.01 * canvas.width
    const halfWidth = size / 2;

    const tip_x = scaledX + size * Math.cos(theta);
    const tip_y = scaledY + size * Math.sin(theta);

    const left_x = scaledX + halfWidth * Math.cos(theta + Math.PI * 0.75);
    const left_y = scaledY + halfWidth * Math.sin(theta + Math.PI * 0.75);

    const right_x = scaledX + halfWidth * Math.cos(theta - Math.PI * 0.75);
    const right_y = scaledY + halfWidth * Math.sin(theta - Math.PI * 0.75);

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

ws.onmessage = (event) => {
    const boids = JSON.parse(event.data);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    boids.forEach(([theta,x,y]) => drawBoid(theta,x,y));
};

function changeLayout() {
    const canvas = document.getElementById("sim-canvas");
    const availableWidth = window.innerWidth - controls_width - (3 * canvas_padding);
    const availableHeight = window.innerHeight - 2 * canvas_padding;
    const size = Math.min(availableWidth, availableHeight);

    canvas.width = size;
    canvas.height = size;

    canvas.style.width = `${size}px`;
    canvas.style.height = `${size}px`;
    console.log('resizing canvas')
}

function sendParameters(){
    if (ws.readyState === WebSocket.OPEN){
        let vals = [k_param.value,s_param.value,a_param.value,c_param.value,]
        ws.send(vals)
    }

} 

function sendReset() {
    ws.send("reset");
}


changeLayout();
window.addEventListener('resize', changeLayout);

s_param.oninput = function() { sendParameters();};
a_param.oninput = function() { sendParameters();};
c_param.oninput = function() { sendParameters();};
k_param.oninput = function() { sendParameters();};
reset_btn.onclick = function() { sendReset();};
const canvas = document.getElementById("swarm-environment");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    const availableWidth = window.innerWidth;
    const availableHeight = window.innerHeight - 200;
    const size = Math.min(availableWidth, availableHeight);

    canvas.width = size;
    canvas.height = size;

    canvas.style.width = `${size}px`;
    canvas.style.height = `${size}px`;
}

function drawBoid(ctx, x, y, theta) {
    // const heading = theta // -theta - Math.PI/2; // make 0 degrees up, convert to radians 
    const size = 15
    const halfWidth = size / 2;

    const tip_x = x + size * Math.cos(theta);
    const tip_y = y + size * Math.sin(theta);

    const left_x = x + halfWidth * Math.cos(theta + Math.PI * 0.75);
    const left_y = y + halfWidth * Math.sin(theta + Math.PI * 0.75);

    const right_x = x + halfWidth * Math.cos(theta - Math.PI * 0.75);
    const right_y = y + halfWidth * Math.sin(theta - Math.PI * 0.75);

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
    console.log("HI")
    ws.send("reset");
});

function sendSliderValues() {
    const values = {
        cohesion: parseFloat(cohesionSlider.value),
        alignment: parseFloat(alignmentSlider.value),
        separation: parseFloat(seperationSlider.value),
        k: parseInt(kSlider.value),
    };
    ws.send(JSON.stringify({ type: "sliders", values }));
}

const kSlider = document.getElementById("k-slider");
const kValue = document.getElementById("k-value");
kValue.textContent = parseInt(kSlider.value);
kSlider.oninput = function() {
    kValue.textContent = this.value;
    sendSliderValues();
};

const cohesionSlider = document.getElementById("cohesion-slider");
const cohesionValue = document.getElementById("cohesion-value");
cohesionValue.textContent = parseFloat(cohesionSlider.value).toFixed(2);
cohesionSlider.oninput = function() {
    cohesionValue.textContent = parseFloat(this.value).toFixed(2);
    sendSliderValues();
};

const alignmentSlider = document.getElementById("alignment-slider");
const alignmentValue = document.getElementById("alignment-value");
alignmentValue.textContent = parseFloat(alignmentSlider.value).toFixed(2);
alignmentSlider.oninput = function() {
    alignmentValue.textContent = parseFloat(this.value).toFixed(2);
    sendSliderValues();
};

const seperationSlider = document.getElementById("seperation-slider");
const seperationValue = document.getElementById("seperation-value");
seperationValue.textContent = parseFloat(seperationSlider.value).toFixed(2);
seperationSlider.oninput = function() {
    seperationValue.textContent = parseFloat(this.value).toFixed(2);
    sendSliderValues();
};


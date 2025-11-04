from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio, random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

agents = [{"x": random.random(), "y": random.random()} for _ in range(2000)]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        for a in agents:
            a["x"] = (a["x"] + (random.random() - 0.5) * 0.02) % 1
            a["y"] = (a["y"] + (random.random() - 0.5) * 0.02) % 1
        await websocket.send_json(agents)
        await asyncio.sleep(0.05)

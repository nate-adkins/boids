import asyncio, socketserver, threading 
import websockets, json, http.server, webbrowser
import math
from helpers import *

COUNT = 100
S = 0
C = 0
A = 0
K = 5

agents = generate_random_states(COUNT)
async def update_swarm():
    speed = 0.005

    for i, a in enumerate(agents):
        neighbors = [agents[idx] for _, idx in k_nearest_neighbors(agents, i, K)]
        centroid = calc_centroid(neighbors)
        avg_heading = calc_avg_heading(neighbors)
        d_theta = cohesion(centroid, a) * C + alignment(avg_heading, a) * A  + seperation(neighbors, a) * S
        
        new_theta = a["theta"] + d_theta
        a["x"] = (a["x"] + speed * math.cos(new_theta)) % 1
        a["y"] = (a["y"] + speed * math.sin(new_theta)) % 1
        a["theta"] = new_theta

async def swarm_handler(ws):
    global agents, C, A, S, K

    async def listen_for_commands():
        global C, A, S, K
        async for message in ws:
            try:
                data = json.loads(message)
                if isinstance(data, dict) and data.get("type") == "sliders":
                    values = data["values"]
                    C = values.get("cohesion", C)
                    A = values.get("alignment", A)
                    S = values.get("separation", S)
                    K = values.get("k", K)
                elif message == "reset":
                    agents[:] = generate_random_states(COUNT)
            except json.JSONDecodeError:
                if message == "reset":
                    agents[:] = generate_random_states(COUNT)


    async def update_loop():
        while True:
            await update_swarm()
            try:
                await ws.send(json.dumps(agents))
            except websockets.ConnectionClosed:
                break
            await asyncio.sleep(0.05)

    await asyncio.gather(update_loop(), listen_for_commands())



async def start_ws_server():
    async with websockets.serve(swarm_handler, "localhost", 8765):
        await asyncio.Future()

def start_http_server():
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer(("localhost", 8000), handler).serve_forever()

def main():
    threading.Thread(target=start_http_server, daemon=True).start()
    # webbrowser.open("http://localhost:8000/swarm.html")
    asyncio.run(start_ws_server())

if __name__ == "__main__":
    main()
    
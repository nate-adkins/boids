import asyncio, random, socketserver, threading 
import websockets, json, http.server, webbrowser
import numpy as np
from math import sin, cos, atan2

COUNT = 200

def generate_random_states():
    return [{"x": random.random(), 
             "y": random.random(), 
             "theta": random.random()*2*np.pi} 
             
             for _ in range(COUNT)]

def angle_diff(a, b):
    '''radians in and out'''
    return (a - b + np.pi) % (2 * np.pi) - np.pi

def calc_centroid(agents):
    length = len(agents)
    return sum([a["x"] for a in agents])/length, sum([a["y"] for a in agents])/length

def calc_avg_heading(agents):
    vx = sum(cos(a['theta']) for a in agents)
    vy = sum(sin(a['theta']) for a in agents)
    return atan2(vy, vx)


cohesion_strength = 0.02
alignment_strength = -0.01
agents = generate_random_states()

async def update_swarm():

    centroid = calc_centroid(agents)
    avg_heading = calc_avg_heading(agents)
    speed = 0.005

    for a in agents:

        angle_to_centroid = atan2((centroid[1] - a["y"]),(centroid[0] - a["x"]))
        cohesion_dtheta = angle_diff(angle_to_centroid, a['theta'])

        alignment_dtheta = angle_diff(avg_heading, a['theta']) 

        d_theta = cohesion_dtheta * cohesion_strength + alignment_dtheta * alignment_strength
        new_theta = a["theta"] + d_theta
        a["x"] = a["x"] + speed * cos(new_theta)
        a["y"] = a["y"] + speed * sin(new_theta)
        a["theta"] = new_theta

async def swarm_handler(ws):
    global agents

    async def listen_for_commands():
        nonlocal ws
        async for message in ws:
            if message == "reset":
                agents[:] = generate_random_states()

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
    webbrowser.open("http://localhost:8000/swarm.html")
    asyncio.run(start_ws_server())

if __name__ == "__main__":
    main()
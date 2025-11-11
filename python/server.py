import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from boids import BoidSwarm
import webbrowser, json, time

# parameter updates
async def recieve_params(msg: str):
    msg = msg.split(",")
    print(msg)
    if msg[0] == 'reset':
        swarm.randomize_states()
    else:
        if msg[0] == 'params':
            try:
                swarm.k = int(msg[1])
                swarm.S = float(msg[2])
                swarm.A = float(msg[3])
                swarm.C = float(msg[4])
            except Exception as e:
                swarm.S = 10
                swarm.S = 0.0
                swarm.A = 0.0
                swarm.C = 0.0


async def recieve_params_handler(ws):
    async for message in ws:
        await recieve_params(message)

# state updates
async def update_state():
    

    if time_it:
        start_time = time.time()
        swarm.update()
        end_time = time.time()
        if update_rate_hz:
            while end_time - start_time < (1/update_rate_hz):
                end_time = time.time()
        print(f"{((end_time - start_time)*1000)}")
        # print(f"n: {swarm.count}, k:{swarm.k}")
    else: swarm.update()

    return json.dumps(swarm.boids.tolist())


async def update_state_handler(ws):
    while True:
        try:
            msg = await update_state()
            if msg:
                await ws.send(msg)
        except ConnectionClosed:
            break

async def handler(websocket):
    swarm_task = asyncio.create_task(update_state_handler(websocket))
    inputs_task = asyncio.create_task(recieve_params_handler(websocket))
    await asyncio.gather(swarm_task, inputs_task)

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()


if __name__ == '__main__':    
    # webbrowser.open("index.html")

    update_rate_hz = None
    time_it = True
    boids_test = 100_000
    k_test = 1000
    swarm = BoidSwarm(boids_test,k_test,0.005,0.1,0.1,0.1)

    asyncio.run(main())
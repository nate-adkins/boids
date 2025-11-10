import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from boids import BoidSwarm
import webbrowser
import json


# # producer example 
# async def produce():
#     await asyncio.sleep(0.001)
#     print('produce')
#     return " "#''.join(random.choice(string.ascii_letters) for _ in range(10))

# async def producer_handler(websocket):
#     while True:
#         try:
#             message = await produce()
#             if message:
#                 await websocket.send(message)
#         except ConnectionClosed:
#             break


# # consumer example 
# async def consume(message):
#     print(message)

# async def consumer_handler(websocket):
#     async for message in websocket:
#         await consume(message)

async def recieve_params(msg: str):
    msg = msg.split(',')
    swarm.S = float(msg[0])
    swarm.A = float(msg[1])
    swarm.C = float(msg[2])

async def recieve_params_handler(ws):
    async for message in ws:
        await recieve_params(message)

# update swarm state  
async def update_state():
    await asyncio.sleep(0.001)
    swarm.update()
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
    # consumer_task = asyncio.create_task(consumer_handler(websocket))
    # producer_task = asyncio.create_task(producer_handler(websocket))
    swarm_task = asyncio.create_task(update_state_handler(websocket))
    inputs_task = asyncio.create_task(recieve_params_handler(websocket))
    await asyncio.gather(swarm_task, inputs_task)

async def main():
    async with serve(handler, "localhost", 8765) as server:
        await server.serve_forever()


if __name__ == '__main__':    
    webbrowser.open("index.html")

    swarm = BoidSwarm(3000,50,0.005,0.1,0.1,0.1)

    asyncio.run(main())
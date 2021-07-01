import asyncio
import websockets
import yaml


config = yaml.load(open("config.yaml"), Loader=yaml.Loader)
PORT = config["port"]


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, '0.0.0.0', PORT)
    )

    asyncio.get_event_loop().run_forever()

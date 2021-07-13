import asyncio
import json
import websockets
import yaml


config = yaml.load(open("config.yaml"), Loader=yaml.Loader)
PORT = config["port"]


async def echo(websocket, path):
    async for message in websocket:
        try:
            message_dict = json.loads(message)
            print("Message received:")
            print(message_dict)
        except json.decoder.JSONDecodeError as e:
            print("Message received, but encountered exception when deserializing json.")
            print(f"Message: {message}")
            print(f"Exception: {e}")
        await websocket.send(message)


if __name__ == "__main__":
    # TODO: Use logger to get better timestamps and log levels
    print("Starting the server")
    start_server = websockets.serve(echo, '0.0.0.0', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

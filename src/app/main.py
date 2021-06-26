import asyncio
import websockets


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, '0.0.0.0', 8081)
    )

    asyncio.get_event_loop().run_forever()

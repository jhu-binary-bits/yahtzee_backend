import asyncio
import logging
import websockets
import yaml
from .event import Event


config = yaml.load(open("config.yaml"), Loader=yaml.Loader)
HOST = config["host"]
PORT = config["port"]


class EventBroker:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    async def broker_messages(self, websocket, path):
        async for message in websocket:
            self.log.info(f"Message received: {message}")
            event = Event(message)
            self.log.info(f"Event timestamp: {event.timestamp}")
            self.log.info(f"Event type: {event.type}")
            self.log.info(f"Event data: {event.data}")
            await websocket.send(message)

    def start_server(self):
        self.log.info("Starting the server")
        start_server = websockets.serve(self.broker_messages, HOST, PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

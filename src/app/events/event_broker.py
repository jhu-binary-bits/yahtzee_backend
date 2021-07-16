import asyncio
import logging
import websockets
from events.event import Event
from util.config import Config


class EventBroker:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.config = Config()

    async def broker_messages(self, websocket, path):
        async for message in websocket:
            self.log.info(f"Message received: {message}")
            event = Event(message)
            if event.is_valid:
                self.log.info("This is a valid event")
            else:
                self.log.warning("This is NOT a valid event")
            await websocket.send(message)

    def start_server(self):
        self.log.info("Starting the server")
        start_server = websockets.serve(self.broker_messages, self.config.HOST, self.config.PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

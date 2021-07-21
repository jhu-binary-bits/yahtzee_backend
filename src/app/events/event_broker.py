import asyncio
import json
import logging
import websockets
from datetime import datetime
from events.event import Event
from engine.game_engine import GameEngine
from util.config import Config


PLAYER_CONNECTIONS = set()    # TODO: Could make some kind of a connections class
ENGINE_EVENTS = [             # TODO: could make this an enum
    "player_joined",
    "player_left",
    "chat_message"
]


class EventBroker:
    def __init__(self, engine: GameEngine):
        self.log = logging.getLogger(__name__)
        self.config = Config()
        self.game_engine = engine

    async def send_game_state_update(self):
        """
        This sends the whole game state whenever it is called. This seems to work well since we can
        pass the whole game state along to each component in React and always use the updated
        version of each variable.
        """
        self.log.info("Sending a game state update to all players")
        if PLAYER_CONNECTIONS:  # asyncio.wait doesn't accept an empty list
            event = self.game_engine.get_game_state_event()
            await asyncio.wait([socket_client.send(event) for socket_client in PLAYER_CONNECTIONS])

    async def register_websocket(self, websocket):
        self.log.info("Client joined, registering websocket")
        PLAYER_CONNECTIONS.add(websocket)

    async def unregister_websocket(self, websocket):
        self.log.info("Client disconnected, unregistering websocket")
        PLAYER_CONNECTIONS.remove(websocket)
        player_left_message = {
            "timestamp": datetime.now().timestamp(),
            "type": "player_left",
            "data": {}   # We don't know the player name yet, figure that out in the state manager
        }
        return json.dumps(player_left_message)

    async def broker(self, websocket, path):
        self.log.info("Brokering messages")
        await self.register_websocket(websocket)
        try:
            # Send initial state to the player who just joined
            await self.send_game_state_update()
            async for message in websocket:
                self.log.info(f"Message received from client: {message}")
                event = Event(message, websocket)
                if event.is_valid:
                    self.log.info("This is a valid event")
                    if event.type in ENGINE_EVENTS:
                        # Process the events in the game engine, which will update parts of the state
                        self.game_engine.process_event(event)
                        await self.send_game_state_update()
                else:
                    self.log.warning("This is NOT a valid event")
        finally:
            # When we lose connection to a websocket, we need to pretend we received a real event from the front end
            mock_message = await self.unregister_websocket(websocket)
            event = Event(mock_message, websocket)
            self.game_engine.process_event(event)
            await self.send_game_state_update()

    def start_server(self):
        self.log.info("Starting the server")
        start_server = websockets.serve(self.broker, self.config.HOST, self.config.PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

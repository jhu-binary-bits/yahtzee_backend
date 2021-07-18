import asyncio
import json
import logging
import websockets
from datetime import datetime
from events.event import Event
from engine.game_engine import GameEngine
from util.config import Config


STATE = {"value": 0}
WEBSOCKETS = set()    # TODO: could use the websockets from the list of players in the state
ENGINE_EVENTS = [     # TODO: could make this an enum
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
        For now, this just sends the whole game state (which is just players and chat) every time.
        If we want, we could adjust this to take a more tailored message from the engine and only
        send messages with information about what has changed.
        """
        self.log.info("Sending a game state update to all players")
        if WEBSOCKETS:  # asyncio.wait doesn't accept an empty list
            event = self.game_engine.get_game_state_event()
            await asyncio.wait([socket_client.send(event) for socket_client in WEBSOCKETS])

    async def register_websocket(self, websocket):
        self.log.info("Client joined, registering websocket")
        WEBSOCKETS.add(websocket)

    async def unregister_websocket(self, websocket):
        self.log.info("Client disconnected, unregistering websocket")
        WEBSOCKETS.remove(websocket)
        player_left_message = {
            "timestamp": datetime.now().timestamp(),
            "type": "player_left",
            "data": {}   # We don't know the player name yet, figure that out in the state manager
        }
        return json.dumps(player_left_message)

    async def broker(self, websocket, path):
        self.log.info("Brokering messages")
        # register(websocket) sends user_event() to websocket
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

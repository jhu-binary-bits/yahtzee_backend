import asyncio
import json
import logging
import websockets
from datetime import datetime

from entities.events import Event
from engine.state_manager import StateManager
from util.config import Config


PLAYER_CONNECTIONS = set()    # TODO: Could make some kind of a connections class


class EventBroker:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.config = Config()
        self.state_manager = StateManager()

    async def send_game_state_update(self):
        """
        This sends the whole game state whenever it is called. This seems to work well since we can
        pass the whole game state along to each component in React and always use the updated
        version of each variable.
        """
        self.log.info("Sending a game state update to all players")
        if PLAYER_CONNECTIONS:  # asyncio.wait doesn't accept an empty list
            event = self.state_manager.publish_current_state()
            await asyncio.wait([socket_client.send(event) for socket_client in PLAYER_CONNECTIONS])
        return self

    async def register_websocket(self, websocket):
        """
        Called whenever a new websocket connection is sent from the front end.
        Adds the new websocket to the set of PLAYER_CONNECTIONS.
        """
        self.log.info("Client joined, registering websocket")
        PLAYER_CONNECTIONS.add(websocket)
        return self

    async def unregister_websocket(self, websocket):
        """
        Called whenever a websocket connection is terminated on the front end.
        Minimal information is sent with the websocket termination, so we manufacture one here.
        """
        self.log.info("Client disconnected, unregistering websocket")
        PLAYER_CONNECTIONS.remove(websocket)
        player_left_message = {
            "timestamp": datetime.utcnow().timestamp() * 1000,
            "type": "player_left",
            "data": {}   # We don't know the player name yet, figure that out in the state manager
        }
        return json.dumps(player_left_message)

    async def broker(self, websocket, path):
        """
        The function that the server calls whenever a message from a websocket on the front end is received.

        1) When a new websocket establishes a connection, register a new player
        2) Send game state update to all players that the new player has joined
        3) Listen for new messages from the websocket
        4) When a new message is received
            * Create an event
            * If it is a valid event, send it to the state manager
            * Send out a game state update after the event is processed
        5) When a websocket connection is closed, create and process a player left event
        """
        self.log.info("Brokering messages")
        # When a new websocket connection is established, register the websocket (create a new player)
        await self.register_websocket(websocket)
        try:
            # Send initial state to the player who just joined
            await self.send_game_state_update()
            # Now, the server sits here waiting for new messages from the websocket
            async for message in websocket:
                # Every time a message is received, do the following
                self.log.info(f"Message received from client: {message}")
                # Create an event
                event = Event(message, websocket)
                if event.is_valid:
                    self.log.info("This is a valid event")
                    # Process the events in the state manager
                    self.state_manager.process_event(event)
                    await self.send_game_state_update()
                else:
                    self.log.warning("This is NOT a valid event")
        except Exception as e:
            # Broad catchall to keep the server alive in the case of an error.
            # Prints the error message and traceback to the logs without raising the Exception and killing the program
            self.log.error(e, exc_info=True)
        finally:
            # When we lose connection to a websocket, we need to pretend we received a real event from the front end
            mock_message = await self.unregister_websocket(websocket)
            event = Event(mock_message, websocket)
            self.state_manager.process_event(event)
            await self.send_game_state_update()

    def start_server(self):
        self.log.info("Starting the server")
        start_server = websockets.serve(self.broker, self.config.HOST, self.config.PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

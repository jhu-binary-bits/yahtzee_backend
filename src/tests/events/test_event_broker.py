"""
import unittest

from src.app.engine.game_engine import GameEngine
from src.app.events.event_broker import EventBroker


class TestEventBroker(unittest.TestCase):
    def setUp(self):
        self.game_engine = GameEngine()
        self.event_broker = EventBroker(engine=self.game_engine)

    async def test_register_websocket(self):
        await self.event_broker.register_websocket("foo")
        await self.event_broker.register_websocket("bar")
        self.assertEqual(2, len(self.event_broker.player_connections))
        self.assertEqual("foo", self.event_broker.player_connections[0])
        self.assertEqual("bar", self.event_broker.player_connections[1])

    async def test_unregister_websocket(self):
        await self.event_broker.register_websocket("foo")
        await self.event_broker.register_websocket("bar")
        await self.event_broker.unregister_websocket("foo")
        self.assertEqual(1, len(self.event_broker.player_connections))
        await self.event_broker.unregister_websocket("bar")
        self.assertEqual(0, len(self.event_broker.player_connections))


if __name__ == '__main__':
    unittest.main()
"""

from unittest import TestCase

from ttt.player import Player


# noinspection PyTypeChecker
class TestPlayer(TestCase):
    player = None

    def setUp(self):
        self.player = Player("T", "X")

    def test_instantiation(self):
        self.assertIsNotNone(self.player)
        self.assertIsInstance(self.player, Player)

    def test_name_getter(self):
        self.assertEqual(self.player.name, "T")

    def test_marker_getter(self):
        self.assertEqual(self.player.marker, "X")

    def test_invalid_name_args(self):
        with self.assertRaises(AssertionError):
            Player(1, "X")

    def test_invalid_marker_args(self):
        with self.assertRaises(AssertionError):
            Player("Test", "-")

    def test_string_notation(self):
        self.assertEqual(str(self.player), "Player name: T marker: X")

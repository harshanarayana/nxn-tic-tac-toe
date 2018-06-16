from unittest import TestCase

from ttt.helper_util import PositionOccupiedException, InvalidCellPosition, \
    AllMovesExhaustedWithNoWinner


class TestHelperUtils(TestCase):

    def test_position_occupied_exception(self):
        e = PositionOccupiedException("Test")
        self.assertEqual(str(e), "Test")

    def test_invalid_cell_exception(self):
        e = InvalidCellPosition("Test")
        self.assertEqual(str(e), "Test")

    def test_moves_exhausted_exception(self):
        e = AllMovesExhaustedWithNoWinner()
        self.assertEqual(str(e), "")

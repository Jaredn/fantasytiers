__author__ = 'Jared'

import unittest
from draftkings import DraftKings


class MyTestCase(unittest.TestCase):
    def test_load_salaries(self):
        dk = DraftKings()
        dk.load_salaries()
        print("DK_Salary Length = ", len(dk.salaries))
        self.assertGreaterEqual(len(dk.salaries), 100)

    def test_get_single_player_data(self):
        dk = DraftKings()
        dk.load_salaries()
        antonio_brown_data = dk.get_single_player_data(playername='Antonio Brown')
        print("Antonio Brown Data = ", antonio_brown_data)
        self.assertGreaterEqual(antonio_brown_data['Salary'], 1000)

if __name__ == '__main__':
    unittest.main()

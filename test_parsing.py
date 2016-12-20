import unittest
import parsing

class TestParsing(unittest.TestCase):
    def test_week(self):
        self.assertTrue(parsing.Parser.week("22"), 22)
        self.assertTrue(parsing.Parser.week(22), 22)
        self.assertTrue(isinstance(parsing.Parser.week('tw'), int))
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.week('td')

unittest.main()

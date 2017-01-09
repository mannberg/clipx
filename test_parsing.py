import unittest
import parsing
import datetime

class TestParsing(unittest.TestCase):

    def test_week(self):
        self.assertEqual(parsing.Parser.week("22"), 22)
        self.assertEqual(parsing.Parser.week(22), 22)
        self.assertTrue(isinstance(parsing.Parser.week('tw'), int))
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.week('td')

    def test_date(self):
        self.assertEqual(parsing.Parser.date("22/10/2016"), datetime.date(2016, 10, 22))
        self.assertEqual(parsing.Parser.date("22/10/2016+1"), datetime.date(2016, 10, 23))
        self.assertEqual(parsing.Parser.date("22/10/2016-1"), datetime.date(2016, 10, 21))
        self.assertTrue(isinstance(parsing.Parser.date("today-1"), datetime.date))
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.date("thisday-1")

unittest.main()

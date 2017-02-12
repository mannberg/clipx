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
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.week(-1)
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.week(128)

    def test_date(self):
        self.assertEqual(parsing.Parser.date("22/10/2016"), datetime.date(2016, 10, 22))
        self.assertEqual(parsing.Parser.date("22/10/2016+1"), datetime.date(2016, 10, 23))
        self.assertEqual(parsing.Parser.date("22/10/2016-1"), datetime.date(2016, 10, 21))
        self.assertTrue(isinstance(parsing.Parser.date("today-1"), datetime.date))
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.date("thisday-1")

    def test_argument_with_offset(self):
        self.assertEqual(parsing.Parser.argument_with_offset("abc-10"), ('abc', -10))
        self.assertEqual(parsing.Parser.argument_with_offset("abc+3"), ('abc', 3))
        self.assertEqual(parsing.Parser.argument_with_offset("abc123"), ('abc123', None))
        self.assertEqual(parsing.Parser.argument_with_offset("+"), ('+', None))
        self.assertEqual(parsing.Parser.argument_with_offset("+++"), ('+++', None))
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.argument_with_offset(2)

    def test_hours(self):
        self.assertEqual(parsing.Parser.hours(2), 2)
        with self.assertRaises(parsing.BadFormatException):
            parsing.Parser.hours('abc')

    def test_project(self):
        projects = ['apple', 'google']
        self.assertEqual(parsing.Parser.project('pple', projects), 'apple')
        with self.assertRaises(parsing.NonExistentProjectException):
            parsing.Parser.project('xxx', projects)
        with self.assertRaises(parsing.NonExistentProjectException):
            parsing.Parser.project(2, projects)

unittest.main()

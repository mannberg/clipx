import unittest
import datetime
from dates import DateHandler

class TestDates(unittest.TestCase):
    def test_date_from_alias(self):
        self.assertTrue(isinstance(DateHandler.date_from_alias('today'), datetime.date))
        self.assertTrue(isinstance(DateHandler.date_from_alias('tomorrow'), datetime.date))
        self.assertTrue(isinstance(DateHandler.date_from_alias('yesterday'), datetime.date))
        self.assertTrue(isinstance(DateHandler.date_from_alias('today', offset=1), datetime.date))
        self.assertTrue(isinstance(DateHandler.date_from_alias('today', offset=-1), datetime.date))

        self.assertEqual(DateHandler.date_from_alias(None), None)
        self.assertEqual(DateHandler.date_from_alias('never'), None)
        self.assertEqual(DateHandler.date_from_alias('today', offset=''), None)

    def test_date_from_string(self):
        self.assertEqual(DateHandler.date_from_string(1, 1), None)
        self.assertEqual(DateHandler.date_from_string('', ''), None)

unittest.main()

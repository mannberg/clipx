import unittest
import interface

class TestInterface(unittest.TestCase):
    def test_action_name_with_arguments(self):
        self.assertEqual(interface.action_name_with_arguments(['px.py', 'add']), ('add', []))
        self.assertEqual(interface.action_name_with_arguments(["px.py", "add", "8"]), ('add', ['8']))
        with self.assertRaises(interface.MissingArgumentException):
            interface.action_name_with_arguments(["px.py"])
        with self.assertRaises(interface.MissingArgumentException):
            interface.action_name_with_arguments([])
        with self.assertRaises(interface.InvalidInputException):
            interface.action_name_with_arguments(2)

unittest.main()

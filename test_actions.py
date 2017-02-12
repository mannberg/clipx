import unittest
import actions

class TestActions(unittest.TestCase):

    def test_get_action(self):
        self.assertTrue(isinstance(actions._get_action('add'), actions.Add))
        with self.assertRaises(actions.InvalidActionException):
            actions._get_action('')
        with self.assertRaises(actions.InvalidActionException):
            actions._get_action(2)

    def test_count_arguments(self):
        self.assertTrue(actions.ReadAction()._count_arguments([1,2,3], range(1,4)) is None)
        self.assertTrue(actions.WriteAction()._count_arguments([1,2,3], 3) is None)
        with self.assertRaises(actions.IncorrectNumberOfArgumentsException):
            actions.ReadAction()._count_arguments([], range(1,4))
        with self.assertRaises(actions.IncorrectNumberOfArgumentsException):
            actions.WriteAction()._count_arguments([1,2], 3)

unittest.main()

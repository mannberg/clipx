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
        self.assertTrue(actions.ReadAction()._count_arguments_range([1,2,3], range(1,4)) is None)
        self.assertTrue(actions.WriteAction()._count_arguments([1,2,3], 3) is None)
        with self.assertRaises(actions.IncorrectNumberOfArgumentsException):
            actions.ReadAction()._count_arguments([], range(1,4))
        with self.assertRaises(actions.IncorrectNumberOfArgumentsException):
            actions.WriteAction()._count_arguments([1,2], 3)

    def test_add(self):
        try:
            actions.execute('add', ['8', 'today', 'apple'])
        except:
            raise
            self.fail()

    def test_del(self):
        try:
            actions.execute('del', ['8', 'today', 'apple'])
        except:
            raise
            self.fail()

    def test_set(self):
        try:
            actions.execute('set', ['8', 'today', 'apple'])
        except:
            raise
            self.fail()

    def test_show(self):
        try:
            actions.execute('show', ['today'])
            actions.execute('show', ['today', 'apple'])
        except:
            raise
            self.fail()

    def test_hours(self):
        try:
            actions.execute('hours', ['today'])
            actions.execute('hours', ['today', 'apple'])
        except:
            raise
            self.fail()

unittest.main()

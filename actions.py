import sys
from dates import DateHandler
from parsing import Parser
import parsing

class ActionException(Exception):
    def __init__(self, arg):
        self.message = arg

class IncorrectNumberOfArgumentsException(ActionException):
    pass

class BadValueException(ActionException):
    pass

class InvalidActionException(ActionException):
    pass

class BadActionArgumentException(ActionException):
    pass

class NonExistentProjectException(ActionException):
    pass

def execute(action_name, args):
    action = get_action(action_name)
    action.perform_if_valid_arguments(args)

def get_action(arg):
    """Return proper action instance

    >>> obj = get_action('add')
    >>> isinstance(obj, Add)
    True

    >>> get_action('')
    Traceback (most recent call last):
    ...
    InvalidActionException

    >>> get_action(2)
    Traceback (most recent call last):
    ...
    InvalidActionException
    """
    try:
        return {
        'add': Add,
        'del': Del,
        'show': Show,
        'hours': Hours
        }[arg]()
    except KeyError:
        raise InvalidActionException("Action " + str(arg) + " does not exist.")

class Action(object):
    pass

class ReadAction(Action):

    def get_validated_arguments(self, args):

        self.count_arguments(args, range(1,3))
        week = self._get_parsed_week(args[0])
        date = self._get_parsed_date(args[0])
        project = None

        if week is None and date is None:
            raise BadValueException("Week number or date, please!")

        try:
            project = self._get_parsed_project(args[1])
        except IndexError:
            pass
        except parsing.NonExistentProjectException:
            raise NonExistentProjectException("")

        return week, date, project

    def count_arguments(self, args, expected_argument_range):
        """
        >>> ReadAction().count_arguments([1,2,3], range(1,4)) is None
        True

        >>> ReadAction().count_arguments([], range(1,4))
        Traceback (most recent call last):
        ...
        IncorrectNumberOfArgumentsException
        """
        if len(args) not in expected_argument_range:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def _get_parsed_week(self, arg):
        try:
            return Parser.week(arg)
        except parsing.BadFormatException:
            return None

    def _get_parsed_date(self, arg):
        try:
            return Parser.date(arg)
        except parsing.BadFormatException as e:
            return None

    def _get_parsed_project(self, arg):
        try:
            return Parser.project(arg)
        except parsing.BadFormatException as e:
            raise BadActionArgumentException(e.message)

class WriteAction(Action):

    def get_validated_arguments(self, args):
        self.count_arguments(args, 3)
        hours, date, project = self._get_parsed_arguments(args)
        self._validate_arguments(hours, date, project)
        return (hours, date, project)

    def count_arguments(self, args, expected_argument_count):
        """
        >>> WriteAction().count_arguments([1,2,3], 3) is None
        True

        >>> WriteAction().count_arguments([1,2], 3)
        Traceback (most recent call last):
        ...
        IncorrectNumberOfArgumentsException
        """
        if len(args) is not expected_argument_count:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def _get_parsed_arguments(self, args):
        try:
            hours = Parser.hours(args[0])
            date = Parser.date(args[1])
            project = Parser.project(args[2])
            return (hours, date, project)
        except parsing.BadFormatException as e:
            raise BadActionArgumentException(e.message)
        except parsing.NonExistentProjectException:
            raise NonExistentProjectException("")

    def _validate_arguments(self, hours, date, project):
        try:
            self._validate_hours(hours)
            self._validate_date(date)
            self._validate_project(project)
        except parsing.BadFormatException as e:
            raise BadActionArgumentException(e.message)

    def _validate_hours(self, hours):
        if hours < 0:
            raise BadValueException("Hours cannot be negative.")
        elif hours >= 99:
            raise BadValueException("Too many hours, man!")

    def _validate_date(self, date):
        if date.year > 2020:
            raise BadValueException("Too far in the future, man...")

    def _validate_project(self, project):
        if project < 0:
            raise BadValueException("Project doesn't exist.")

class Add(WriteAction):

    def perform_if_valid_arguments(self, args):
        hours, date, project = self.get_validated_arguments(args)
        self._add(hours, date, project)

    def _add(self, hours, date, project):
        print "Added %d hours to project %s for date %s." % (hours, str(project), str(date))

class Del(WriteAction):
    def perform_if_valid_arguments(self, args):
        hours, date, project = self.get_validated_arguments(args)
        self._del(hours, date, project)

    def _del(self, hours, date, project):
        print "Deleted %d hours to project %s for date %s." % (hours, str(project), str(date))

class Show(ReadAction):

    def perform_if_valid_arguments(self, args):
        week, date, project = self.get_validated_arguments(args)

        if week is not None:
            self._show_week(week)
        elif date is not None:
            self._show_date(date)

        if project is not None:
            self._show_project(project)

    def _show_week(self, week):
        print "Showing week " + str(week) + " ..."

    def _show_date(self, date):
        print "Showing date " + str(date)

    def _show_project(self, project):
        print "For project " + project

class Hours(ReadAction):
    
    def perform_if_valid_arguments(self, args):
        week, date, project = self.get_validated_arguments(args)

        if week is not None:
            self._show_week(week)
        elif date is not None:
            self._show_date(date)

        if project is not None:
            self._show_project(project)

    def _show_week(self, week):
        print "Showing hours for week " + str(week) + " ..."

    def _show_date(self, date):
        print "Showing hours for date " + str(date)

    def _show_project(self, project):
        print "For project " + project

if __name__ == "__main__":
    import doctest
    doctest.testmod()

import sys
from abc import ABCMeta, abstractmethod
from dates import DateHandler
from parsing import Parser
import parsing
import storage

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
    action = _get_action(action_name)
    action.perform_if_valid_arguments(args)

def _get_action(arg):
    """Return proper action instance"""

    try:
        return {
        'set': Set,
        'show': Show,
        'hours': Hours,
        'addproj': AddProject,
        'lsproj': ListProjects
        }[arg.lower()]()
    except (KeyError, AttributeError):
        raise InvalidActionException("Action " + str(arg) + " does not exist.")

class Action(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform_if_valid_arguments():
        pass

    @abstractmethod
    def get_valid_arguments():
        pass

    @abstractmethod
    def _validate_arguments():
        pass

    @abstractmethod
    def _parse_arguments():
        pass

    def _count_arguments(self, args, expected_argument_count):
        if len(args) is not expected_argument_count:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def _count_arguments_range(self, args, expected_argument_range):
        if len(args) not in expected_argument_range:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def validate_hours(self, hours):
        if hours < 0:
            raise BadValueException("Hours cannot be negative.")
        elif hours >= 99:
            raise BadValueException("Too many hours, man!")

    def validate_date(self, date):
        if date.year > 2020:
            raise BadValueException("Too far in the future, man...")

    def validate_project(self, project):
        if project < 0:
            raise BadValueException("Project doesn't exist.")

    def parsed_week(self, arg):
        try:
            return Parser.week(arg)
        except parsing.BadFormatException:
            return None

    def parsed_date(self, arg):
        try:
            return Parser.date(arg)
        except parsing.BadFormatException:
            return None

    def parsed_project(self, arg):
        try:
            return Parser.project(arg)
        except parsing.BadFormatException as e:
            raise BadActionArgumentException(e.message)

class ReadAction(Action):

    def perform_if_valid_arguments(self, args):
        pass

    def get_valid_arguments(self, args):
        self._count_arguments_range(args, range(1,3))
        week, date, project = self._parse_arguments(args)
        self._validate_arguments(date, project)
        return week, date, project

    def _parse_arguments(self, args):
        week = self.parsed_week(args[0])
        date = self.parsed_date(args[0])
        project = None

        if week is None and date is None:
            raise BadValueException("Week number or date, please!")

        try:
            project = self.parsed_project(args[1])
        except IndexError:
            pass
        except parsing.NonExistentProjectException:
            raise NonExistentProjectException("")

        return week, date, project

    def _validate_arguments(self, date, project):
        try:
            if date is not None:
                self.validate_date(date)
            if project is not None:
                self.validate_project(project)
        except parsing.BadFormatException as e:
            raise BadActionArgumentException(e.message)

class WriteAction(Action):

    def perform_if_valid_arguments(self, args):
        pass

    def get_valid_arguments(self, args):
        self._count_arguments(args, 3)
        hours, date, project = self._parse_arguments(args)
        self._validate_arguments(hours, date, project)
        return hours, date, project

    def _parse_arguments(self, args):
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
            self.validate_hours(hours)
            self.validate_date(date)
            self.validate_project(project)
        except parsing.BadFormatException as e:
            raise BadActionArgumentException(e.message)

class Set(WriteAction):

    def perform_if_valid_arguments(self, args):
        hours, date, project = self.get_valid_arguments(args)
        self._set(hours, date, project)

    def _set(self, hours, date, project):
        print "Set project {} to {} hours for date {}.".format(str(project), hours, str(date))

class AddProject(Action):

    def perform_if_valid_arguments(self, args):
        self._count_arguments(args, 1)
        project = self.get_valid_arguments(args[0])

        def success():
            print "Added project"

        storage.add_project(project, success)

    def _validate_arguments():
        pass

    def get_valid_arguments(self, project):
        if not isinstance(project, str):
            raise BadActionArgumentException("")
        return project

    def _parse_arguments(self, args):
        pass

class ListProjects(Action):

    def perform_if_valid_arguments(self, args):
        self._count_arguments(args, 0)
        storage.list_projects()

    def _validate_arguments():
        pass

    def get_valid_arguments(self, project):
        pass

    def _parse_arguments(self, args):
        pass

class Show(ReadAction):

    def perform_if_valid_arguments(self, args):
        week, date, project = self.get_valid_arguments(args)

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
        week, date, project = self.get_valid_arguments(args)

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

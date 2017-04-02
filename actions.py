import sys
from abc import ABCMeta, abstractmethod
from parsing import Parser
import parsing
import storage

class ActionException(Exception):
    def __init__(self, arg):
        self.message = arg

class IncorrectNumberOfArgumentsException(ActionException):
    pass

class InvalidActionException(ActionException):
    pass

class BadArgumentException(ActionException):
    pass

class ExecutionFailureException(ActionException):
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
    def validate_arguments():
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

    #TODO: Remove! Already done in Parser
    def _validate_date(self, date):
        if len(str(date.year)) is not 4:
            raise BadArgumentException("Too far in the future, man...")

class ReadAction(Action):

    def perform_if_valid_arguments(self, args):
        pass

    def validate_arguments(self, args):
        self._count_arguments_range(args, range(1,3))
        week, date, project = self._parse_arguments(args)
        return week, date, project

    def _parse_arguments(self, args):
        week = date = project = None

        try:
            week = Parser.week(args[0])
        except parsing.BadFormatException:
            pass

        try:
            date = Parser.date(args[0])
        except parsing.BadFormatException:
            pass

        if week is None and date is None:
            raise BadArgumentException("Week number or date, please!")

        try:
            project = Parser.project(args[1])
        except (IndexError, parsing.BadFormatException):
            pass

        return week, date, project

class WriteAction(Action):

    def perform_if_valid_arguments(self, args):
        pass

    def validate_arguments(self, args):
        self._count_arguments(args, 3)
        hours, date, project = self._parse_arguments(args)
        return hours, date, project

    def _parse_arguments(self, args):
        try:
            hours = Parser.hours(args[0])
            date = Parser.date(args[1])
            project = Parser.project(args[2])
            return hours, date, project
        except parsing.BadFormatException as e:
            raise BadArgumentException(e.message)

class Set(WriteAction):

    def perform_if_valid_arguments(self, args):
        hours, date, project = self.validate_arguments(args)
        self._set(hours, date, project)

    def _set(self, hours, date, project):
        try:
            storage.set_hours(hours, date, project)
        except storage.NonExistentProjectError:
            raise BadArgumentException("")

class AddProject(Action):

    def perform_if_valid_arguments(self, args):
        project = self.validate_arguments(args)
        self._add_project(project)

    def _add_project(self, project):
        try:
            storage.add_project(project)
        except:
            raise ExecutionFailureException

    def validate_arguments(self, args):
        self._count_arguments(args, 1)
        project = self._parse_arguments(args)
        return project

    def _parse_arguments(self, args):
        try:
            return Parser.project(args[0])
        except parsing.BadFormatException as e:
            raise BadArgumentException(e.message)

class ListProjects(Action):

    def perform_if_valid_arguments(self, args):
        self._count_arguments(args, 0)
        projects = storage.list_projects()
        for p in projects:
            print p

    def validate_arguments(self, project):
        pass

    def _parse_arguments(self, args):
        pass

class Show(ReadAction):

    def perform_if_valid_arguments(self, args):
        week, date, project = self.validate_arguments(args)
        if week is not None:
            self._show_week(week)
        elif date is not None:
            self._show_date(date, project)

    def _show_week(self, week):
        print "Showing week " + str(week) + " ..."

    def _show_date(self, date, project):
        try:
            if project is not None:
                workday = storage.show_date_for_project(date, project)
            else:
                workday = storage.show_date(date)

            print self.success_string(workday[1], workday[2])
        except storage.NonExistentProjectError:
            raise BadArgumentException("No project named {}".format(project))
        except storage.NoWorkdaysForDateError:
            raise BadArgumentException("No days for date {}".format(str(date)))
        except IndexError:
            raise BadArgumentException("Something went wrong.")

    def success_string(self, hours, date):
        try:
            return "### {} : {} hours ###".format(str(date), str(hours))
        except:
            pass

class Workday():
    def __init__(self, hours, date, project_name):
        self.hours = hours
        self.date = date
        self.project_name = project_name

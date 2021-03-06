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

    description = ""

    def _count_arguments(self, args, expected_argument_count):
        if len(args) is not expected_argument_count:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def _count_arguments_range(self, args, expected_argument_range):
        if len(args) not in expected_argument_range:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

class ReadAction(Action):

    def _validate_arguments(self, args):
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

    def _validate_arguments(self, args):
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
        hours, date, project = self._validate_arguments(args)
        self._set(hours, date, project)

    def _set(self, hours, date, project):
        try:
            storage.set_hours(hours, date, project)
        except storage.NonExistentProjectError:
            raise BadArgumentException("Project does not exist")

class AddProject(Action):

    def perform_if_valid_arguments(self, args):
        project = self._validate_arguments(args)
        self._add_project(project)

    def _add_project(self, project):
        try:
            storage.add_project(project)
        except:
            raise ExecutionFailureException("Failed to add project")

    def _validate_arguments(self, args):
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
        #TODO: Reading from DB should handle exceptions
        projects = storage.list_projects()
        #TODO: This module should not print stuff?
        for p in projects:
            print p

    #Save point

class Show(ReadAction):

    def perform_if_valid_arguments(self, args):
        week, date, project = self._validate_arguments(args)
        if week is not None:
            self._show_week(week, project)
        elif date is not None:
            self._show_date(date, project)

    def _show_week(self, week, project):
        try:
            if project is not None:
                workdays = storage.show_dates_for_week_and_project(week, project)
                print self.success_string_specific_project(workdays)
            else:
                workdays = storage.show_dates_for_week(week)
                print self.success_string_all_projects(workdays)

            if workdays is None:
                raise IndexError

        except storage.NonExistentProjectError:
            raise BadArgumentException("No project named {}".format(project))
        except storage.NoWorkdaysForDateError:
            pass
        except IndexError:
            raise BadArgumentException("Something went wrong.")

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
            print self.success_string(0, date)
        except IndexError:
            raise BadArgumentException("Something went wrong.")

    def success_string(self, hours, date):
        try:
            return "### {} : {} hours ###".format(str(date), str(hours))
        except:
            pass

    def success_string_specific_project(self, days):
        try:
            string = "\n"
            for day in days:
                string += "### Project: {} - {} : {} hours ###\n".format(str(day[0]), str(day[2]), str(day[1]))
            return string
        except:
            raise

    def success_string_all_projects(self, days):
        try:
            string = "\n"
            for pid, hours in days.iteritems():
                for date, hour in hours.iteritems():
                    string += "### Project: {} - {} : {} hours ###\n".format(str(pid), date, str(hour))
            return string
        except:
            raise

class Workday():
    def __init__(self, hours, date, project_name):
        self.hours = hours
        self.date = date
        self.project_name = project_name

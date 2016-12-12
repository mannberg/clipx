import sys
from dates import DateHandler
from parsing import ArgumentParser, BadFormatException

class ActionException(Exception):
    def __init__(self, arg):
        self.message = arg

class IncorrectNumberOfArgumentsException(ActionException):
    pass

class BadValueException(ActionException):
    pass

class InvalidActionException(ActionException):
    pass

def get_action(arg):
    try:
        return {
        'add': Add,
        'del': Delete,
        'show': Show
        }[arg]()
    except:
        raise InvalidActionException("Action " + arg + " does not exist.")

class Action(object):

    def count_arguments(self, args, expected_number_of_args):
        if len(args) != expected_number_of_args:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

class Add(Action):

    def perform_if_valid_arguments(self, args):
        super(Add, self).count_arguments(args, 3)
        hours, date, project = self.__get_parsed_arguments(args)
        self.__validate_arguments(hours, date, project)
        self.__add(hours, date, project)

    def name():
        return 'add'

    def __add(self, hours, date, project):
        print "Added %d hours to project %s for date %s." % (hours, str(project), str(date))

    def __get_parsed_arguments(self, args):
        try:
            hours = ArgumentParser.parse_hours(args[0])
            date = ArgumentParser.parse_date(args[1])
            project = ArgumentParser.parse_project(args[2])
            return (hours, date, project)
        except BadFormatException as e:
            print e.message
            sys.exit()

    def __validate_arguments(self, hours, date, project):
        try:
            self.__validate_hours(hours)
            self.__validate_date(date)
            self.__validate_project(project)
        except BadValueException as e:
            print e.message
            sys.exit()

    def __validate_hours(self, hours):
        if hours < 0:
            raise BadValueException("Hours cannot be negative.")
        elif hours >= 99:
            raise BadValueException("Too many hours, man!")

    def __validate_date(self, date):
        if date.year > 2020:
            raise BadValueException("Too far in the future, man...")

    def __validate_project(self, project):
        if project < 0:
            raise BadValueException("Project doesn't exist.")

class Delete(Action):
    pass

class Show(Action):

    def count_arguments(self, args, expected_arg_range):
        if len(args) not in expected_arg_range:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def name():
        return 'show'

    def perform_if_valid_arguments(self, args):
        self.count_arguments(args, range(1,3))
        week = self.__get_parsed_week(args[0])
        date = self.__get_parsed_date(args[0])

        if week is not None:
            self.__show_week(str(week))
        elif date is not None:
            self.__show_date(str(date))
        else:
            raise BadValueException("Week number or date, please!")

        try:
            project = self.__get_parsed_project(args[1])
            if project is not None:
                self.__show_project(project)
        except IndexError:
            pass

    def __show_week(self, week):
        print "Showing week " + week + " ..."

    def __show_date(self, date):
        print "Showing date " + date

    def __show_project(self, project):
        print "For project " + project

    def __get_parsed_week(self, arg):
        try:
            return ArgumentParser.parse_week(arg)
        except BadFormatException:
            pass

    def __get_parsed_date(self, arg):
        try:
            return ArgumentParser.parse_date(arg)
        except BadFormatException:
            pass

    def __get_parsed_project(self, arg):
        try:
            return ArgumentParser.parse_project(arg)
        except BadFormatException:
            pass

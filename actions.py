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

    number_of_arguments = 0

    def count_arguments(self, args):
        if len(args) != self.number_of_arguments:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

class Add(Action):

    number_of_arguments = 3
    name = 'add'

    def perform_if_valid_arguments(self, args):
        super(Add, self).count_arguments(args)
        parsed_arguments = self.__get_parsed_arguments(args)
        validated_args = self.__sanity_check_arguments(parsed_arguments)
        self.__perform(validated_args)

    def __perform(self, args):
        hours = args[0]
        date = args[1]
        project = args[2]

        print "Added %d hours to project %s for date %s." % (hours, str(project), str(date))

    def __get_parsed_arguments(self, args):
        try:
            hours = ArgumentParser.parse_hours(args[0])
            date = ArgumentParser.parse_date(args[1])
            project = ArgumentParser.parse_project(args[2])
            return [hours, date, project]
        except BadFormatException as e:
            print e.message
            sys.exit()

    def __sanity_check_arguments(self, args):
        try:
            hours = self.__sanity_check_hours(args[0])
            date = self.__sanity_check_date(args[1])
            project = self.__sanity_check_project(args[2])

            return [hours, date, project]
        except BadValueException as e:
            print e.message
            sys.exit()

    def __sanity_check_hours(self, hours):
        if hours > 0 and hours <= 99:
            return hours
        elif hours < 0:
            raise BadValueException("Hours cannot be negative.")
        elif hours >= 99:
            raise BadValueException("Too many hours, man!")

    def __sanity_check_date(self, date):
        if date.year <= 2020:
            return date

        raise BadValueException("Too far in the future, man...")

    def __sanity_check_project(self, project):
        if project > 0:
            return project

        raise BadValueException("Project doesn't exist.")

class Delete(Action):
    pass

class Show(Action):
    #show week, date
    number_of_arguments = range(1,3)
    name = 'show'

    def count_arguments(self, args):
        if len(args) not in self.number_of_arguments:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def perform_if_valid_arguments(self, args):
        self.count_arguments(args)
        parsed_arguments = self.__get_parsed_arguments(args)

        if 'week' in parsed_arguments.keys():
            self.__show_week(str(parsed_arguments['week']))
        elif 'date' in parsed_arguments.keys():
            self.__show_date(str(parsed_arguments['date']))

        if 'project' in parsed_arguments.keys():
            self.__show_project(parsed_arguments['project'])

    def __show_week(self, week):
        print "Showing week " + week + " ..."

    def __show_date(self, date):
        print "Showing date " + date

    def __show_project(self, project):
        print "For project " + project

    def __add_project_to_dictionary(self, dict, args):
        try:
            project = ArgumentParser.parse_project(args[1])
            dict['project'] = project
        except IndexError:
            pass

        return dict

    def __get_parsed_arguments(self, args):
        try:
            week = ArgumentParser.parse_week(args[0])
            if week is not None:
                dict = self.__add_project_to_dictionary({'week': week}, args)

                return dict

            date = ArgumentParser.parse_date(args[0])
            if date is not None:
                dict = self.__add_project_to_dictionary({'date': date}, args)

                return dict

        except BadFormatException as e:
            print e.message
            sys.exit()

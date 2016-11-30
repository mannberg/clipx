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

class Action:
    pass

class Add(Action):

    number_of_arguments = 3
    name = 'add'

    def __count_arguments(self, args):
        if len(args) != self.number_of_arguments:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def perform_if_valid_arguments(self, args):
        self.__count_arguments(args)
        parsed_arguments = self.__parse_arguments(args)
        validated_args = self.__sanity_check_arguments(parsed_arguments)
        self.__add(validated_args)

    def __add(self, args):

        hours = args[0]
        date = args[1]
        project = args[2]

        print("Added %d hours to project %s for date %s." % (hours, str(project), str(date)))

    def __parse_arguments(self, args):
        try:
            hours = ArgumentParser.parse_hours(args[0])
            date = ArgumentParser.parse_date(args[1])
            project = ArgumentParser.parse_project(args[2])
            return [hours, date, project]
        except BadFormatException as e:
            print(e.message)
            sys.exit()

    def __sanity_check_arguments(self, args):
        try:
            hours = self.__sanity_check_hours(args[0])
            date = self.__sanity_check_date(args[1])
            project = self.__sanity_check_project(args[2])

            return [hours, date, project]
        except BadValueException as e:
            print(e.message)
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

    def __count_arguments(self, args):
        if len(args) not in self.number_of_arguments:
            raise IncorrectNumberOfArgumentsException("Incorrect number of arguments.")

    def perform_if_valid_arguments(self, args):
        self.__count_arguments(args)
        parsed_arguments = self.__parse_arguments(args)

        if 'week' in parsed_arguments.keys():
            print("Showing week " + str(parsed_arguments['week']) + " ...")
            if 'project' in parsed_arguments.keys():
                print("For project " + parsed_arguments['project'])
        elif 'date' in parsed_arguments.keys():
            print("Showing date " + str(parsed_arguments['date']))

    def __parse_arguments(self, args):
        try:
            week = ArgumentParser.parse_week(args[0])
            if week is not None:
                print("was week!")
                dict = {'week': week}
                try:
                    project = ArgumentParser.parse_project(args[1])
                    dict['project'] = project
                except IndexError:
                    print "no fucking second..."

                return dict

            date = ArgumentParser.parse_date(args[0])
            if date is not None:
                print("was date!")
                dict = {'date': date}
                try:
                    project = ArgumentParser.parse_project(args[1])
                    dict['project'] = project
                except IndexError:
                    print "no fucking second..."

                return dict

        except BadFormatException as e:
            print(e.message)
            sys.exit()

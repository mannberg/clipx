from dates import DateHandler

class BadFormatException(Exception):
    def __init__(self, arg):
        self.message = arg

class ArgumentParser:

    @staticmethod
    def parse_project(arg):

        projects = ['apple', 'microsoft']

        for p in projects:
            if p.find(arg.lower()) != -1:
                return p

        raise BadFormatException("Faulty project format")

    @staticmethod
    def parse_date(arg):
        offset, stripped_arg = ArgumentParser.argument_has_offset(arg)
        transformed_offset = DateHandler.offset_from_alias(stripped_arg, offset)
        date_from_alias = DateHandler.date_from_alias(stripped_arg, transformed_offset)
        if date_from_alias is not None:
            return date_from_alias

        for frmt in ("%d-%m-%Y", "%d.%m.%Y", "%d/%m/%Y"):
            try:
                date = DateHandler.date_from_string(stripped_arg, frmt, transformed_offset)
                return date
            except ValueError:
                pass

        raise BadFormatException("Faulty date format")

    @staticmethod
    def argument_has_offset(arg):
        try:
            index = [i for i, v in enumerate(arg) if '+' in v or '-' in v][0]
            offset = int(arg[index:])
            stripped_arg = arg[:index]
            return offset, stripped_arg
        except ValueError:
            print "Fanns ej"
            return None, arg
        except IndexError:
            print "Fanns ej + eller minus"
            return None, arg

    @staticmethod
    def parse_hours(arg):
        try:
            hours = int(arg)
            return hours
        except:
            raise BadFormatException("Faulty hour format")

    @staticmethod
    def parse_week(arg):
        offset, stripped_arg = ArgumentParser.argument_has_offset(arg)
        week_from_alias = DateHandler.week_from_alias(stripped_arg, offset)
        if week_from_alias is not None:
            return week_from_alias

        try:
            week = int(stripped_arg)
            if week in range(1,53):
                return week
        except:
            raise BadFormatException("Faulty week format")

    @staticmethod
    def __digits_in_int(i):
        return len(str(i))

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
        date_from_alias = DateHandler.date_from_alias(arg)
        if date_from_alias is not None:
            return date_from_alias

        for frmt in ("%d-%m-%Y", "%d.%m.%Y", "%d/%m/%Y"):
            try:
                return DateHandler.date_from_string(arg, frmt)
            except ValueError:
                pass

        raise BadFormatException("Faulty date format")

    @staticmethod
    def parse_hours(arg):
        try:
            hours = int(arg)
            return hours
        except:
            raise BadFormatException("Faulty hour format")

    @staticmethod
    def parse_week(arg):
        if str(arg) in ['tw']:
            return DateHandler.current_week()

        try:
            week = int(arg)
            if ArgumentParser.__digits_in_int(week) in range(1,3):
                return week
        except:
            raise BadFormatException("Faulty week format")

    @staticmethod
    def __digits_in_int(i):
        return len(str(i))

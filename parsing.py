from dates import DateHandler

class BadFormatException(Exception):
    def __init__(self, arg):
        self.message = arg

class NonExistentProjectException(Exception):
    pass

class Parser:

    @staticmethod
    def week(arg):
        arg = str(arg)
        stripped_arg, offset = Parser.argument_with_offset(arg)
        week_from_alias = DateHandler.week_from_alias(stripped_arg, offset)
        if week_from_alias is not None:
            return week_from_alias

        try:
            week = int(stripped_arg)
            if week in range(1,53):
                return week
            else:
                raise BadFormatException("Not a valid week")
        except ValueError:
            raise BadFormatException("Not a valid week")

    @staticmethod
    def date(arg):
        stripped_arg, offset = Parser.argument_with_offset(arg)
        transformed_offset = DateHandler.day_offset_from_alias(stripped_arg, offset)
        date_from_alias = DateHandler.date_from_alias(stripped_arg, transformed_offset)
        if date_from_alias is not None:
            return date_from_alias

        valid_date_formats = [
            "%d-%m-%Y",
            "%d.%m.%Y",
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%Y.%m.%d",
            "%Y/%m/%d"
        ]
        for frmt in valid_date_formats:
            try:
                date = DateHandler.date_from_string(stripped_arg, frmt, transformed_offset)
                return date
            except ValueError:
                pass

        raise BadFormatException("Not a valid date")

    @staticmethod
    def argument_with_offset(arg):
        try:
            divisor_index = arg.rfind('+')
            if divisor_index is -1 and arg.count('-') is not 2:
                divisor_index = arg.rfind('-')
            if divisor_index is -1:
                raise ValueError

            offset = int(arg[divisor_index:])
            stripped_arg = arg[:divisor_index]
            return stripped_arg, offset
        except (ValueError, IndexError):
            return arg, None
        except (TypeError, AttributeError):
            raise BadFormatException("Expected string, got int")

    @staticmethod
    def project(arg, projects=None):
        arg = str(arg)

        if projects is None:
            projects = ['apple', 'microsoft']

        for p in projects:
            if p.find(arg.lower()) != -1:
                return p

        raise NonExistentProjectException()

    @staticmethod
    def hours(arg):
        try:
            hours = int(arg)
            return hours
        except:
            raise BadFormatException("Not valid hours")

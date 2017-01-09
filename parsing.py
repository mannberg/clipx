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
        except ValueError:
            raise BadFormatException("Not a valid week")

    @staticmethod
    def date(arg):
        stripped_arg, offset = Parser.argument_with_offset(arg)
        transformed_offset = DateHandler.day_offset_from_alias(stripped_arg, offset)
        date_from_alias = DateHandler.date_from_alias(stripped_arg, transformed_offset)
        if date_from_alias is not None:
            return date_from_alias

        for frmt in ("%d-%m-%Y", "%d.%m.%Y", "%d/%m/%Y"):
            try:
                date = DateHandler.date_from_string(stripped_arg, frmt, transformed_offset)
                return date
            except ValueError:
                pass

        raise BadFormatException("Not a valid date")

    @staticmethod
    def argument_with_offset(arg):
        """
        >>> Parser.argument_with_offset("abc-10")
        ('abc', -10)

        >>> Parser.argument_with_offset("abc+3")
        ('abc', 3)

        >>> Parser.argument_with_offset("abc123")
        ('abc123', None)

        >>> Parser.argument_with_offset("+")
        ('+', None)

        >>> Parser.argument_with_offset("+++")
        ('+++', None)

        >>> Parser.argument_with_offset(2)
        Traceback (most recent call last):
        ...
        BadFormatException
        """
        try:
            divisor_index = [i for i, v in enumerate(arg) if '+' in v or '-' in v][0]
            offset = int(arg[divisor_index:])
            stripped_arg = arg[:divisor_index]
            return stripped_arg, offset
        except (ValueError, IndexError):
            return arg, None
        except TypeError:
            raise BadFormatException("Expected string, got int")

    @staticmethod
    def project(arg):
        """
        >>> Parser.project('pple')
        'apple'

        >>> Parser.project('xxx')
        Traceback (most recent call last):
        ...
        NonExistentProjectException

        >>> Parser.project(2)
        Traceback (most recent call last):
        ...
        NonExistentProjectException
        """

        arg = str(arg)

        projects = ['apple', 'microsoft']
        for p in projects:
            if p.find(arg.lower()) != -1:
                return p

        raise NonExistentProjectException()

    @staticmethod
    def hours(arg):
        """
        >>> Parser.hours(2)
        2

        >>> Parser.hours('abc')
        Traceback (most recent call last):
        ...
        BadFormatException
        """
        try:
            hours = int(arg)
            return hours
        except:
            raise BadFormatException("Not valid hours")


if __name__ == "__main__":
    import doctest
    doctest.testmod()

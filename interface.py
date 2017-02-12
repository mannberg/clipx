import actions

"""Get input, show output"""

class MissingArgumentException(Exception):
    pass

class InvalidInputException(Exception):
    pass

def parse_input(args):
    try:
        action_name, args = action_name_with_arguments(args)
        actions.execute(action_name, args)
    except (MissingArgumentException, InvalidInputException):
        print usage_info()
    except actions.InvalidActionException:
        print "No such action."
    except actions.BadValueException as e:
        print e.message
    except actions.IncorrectNumberOfArgumentsException:
        print "Incorrect number of arguments"
    except actions.BadActionArgumentException as e:
        print "Incorrect argument type:", e.message
    except actions.NonExistentProjectException:
        print "Project does not exist."

def action_name_with_arguments(args):
    """Strip script name from arg string"""

    try:
        del args[0]
        action = args.pop(0)
        return action, args
    except IndexError:
        raise MissingArgumentException()
    except TypeError:
        raise InvalidInputException()

def usage_info():
    return """\
    Usage: px [OPTIONS]
        add [hours] [date] [project name]
        del [hours] [date] [project name]
        """

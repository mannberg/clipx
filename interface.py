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
    except actions.ActionException as e:
        print e.message

def action_name_with_arguments(args):
    """Strip script name & arguments from arg string"""

    try:
        del args[0]
        action = args.pop(0)
        return action, args
    except IndexError:
        raise MissingArgumentException()
    except TypeError:
        raise InvalidInputException()

def usage_info():
    indent = ' ' * 4
    string = "\n"
    string = string + "#### CliPX - Time tracking tool for the command line ####" + '\n\n'
    string = string + indent + 'px set <hours> <date> <project_name>' + '\n'
    string = string + indent + 'px show <hours> <(date | week_number)> [<project_name>]' + '\n'
    string = string + indent + 'px addproj <project_name>' + '\n'
    string = string + indent + 'px lsproj' + '\n'
    string = string + '\n'
    string = string + indent + '{:<10}'.format('set') + 'Set number of hours worked on a date for specific project' + '\n'
    string = string + indent + '{:<10}'.format('show') + 'Show number of hours worked on a date or in a week, either for all or specific project(s)' + '\n'
    string = string + indent + '{:<10}'.format('addproj') + 'Add new project' + '\n'
    string = string + indent + '{:<10}'.format('lsproj') + 'List all saved projects' + '\n'
    return string

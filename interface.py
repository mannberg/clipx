import sys
import actions

def get_input():
    args = get_args()
    try:
        verb = args.pop(0)
        action = actions.get_action(str(verb))
        action.perform_if_valid_arguments(args)
    except IndexError:
        print(usage_info())
    except (actions.InvalidActionException, actions.IncorrectNumberOfArgumentsException) as e:
        print(e.message)

def usage_info():
    return """\
    Usage: px [OPTIONS]
        add [hours] [date] [project name]
        del [hours] [date] [project name]
        """

def get_args():
    args = sys.argv
    del args[0]
    return args

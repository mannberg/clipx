import actions

def get_input(args):
    del args[0]
    try:
        verb = action_argument(args)
        action = actions.get_action(str(verb))
        action.perform_if_valid_arguments(args)
    except IndexError:
        print usage_info()
    except (
    actions.InvalidActionException,
    actions.IncorrectNumberOfArgumentsException,
    actions.BadValueException) as e:
        print e.message

def usage_info():
    return """\
    Usage: px [OPTIONS]
        add [hours] [date] [project name]
        del [hours] [date] [project name]
        """

def action_argument(args):
    return args.pop(0)

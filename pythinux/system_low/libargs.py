class ArgumentError(Exception):
    pass
class Manager:
    """
    Argument manager class. Instantiate, add tokens using the add() method, and pass args 
    to the run() method to execute.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tokens = []
    def add(self, token):
        self.tokens.append(token)
    def run(self, args):
        SWITCHES = []
        ARGUMENTS = {}
        ISARGS = bool(len(args))
        for token in self.tokens:
            if isinstance(token, Switch):
                if token.test(args):
                    SWITCHES.append(token.full_name)
        return SWITCHES, ARGUMENTS, ISARGS
    def print_help(self):
        div()
        print("{} [args]".format(self.name))
        div()
        print(self.description)
        div()
        print("Positional arguments:")
        for token in self.tokens:
            if isinstance(token, Switch):
                print("--{}, -{}: {}".format(token.full_name, token.short_name, token.description))
        div()

class Switch:
    """
    A basic switch argument.
    Example: Switch('recursive', 'r', 'Enables recursion')
    When the above example is used, both --recursive and -r are accepted.
    NOTE: when the Manager class returns SWITCHES, the full_name attribute is always appended.
    """
    def __init__(self, full_name, short_name, description):
        self.full_name = full_name
        self.short_name = short_name
        self.description = description
    def test(self, args):
        if "--{}".format(self.full_name) in args:
            return True
        elif "-{}".format(self.short_name) in args:
            return True
        else:
            return False


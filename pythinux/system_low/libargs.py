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
            elif isinstance(token, Option):
                for arg in args:
                    if token.test(arg):
                        lenToRemove = len("--{}=".format(self.name))
                        ARGUMENTS[token.name] = arg[lenToRemove:]
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
                print("{}: {}".format(token.full_name, token.description))
        div()

class Switch:
    """
    A basic switch argument.
    Example: Switch('--recursive', 'Enables recursion')
    When the above example is used, --recursive is accepted.
    NOTE: when the Manager class returns SWITCHES, the full_name attribute is always appended.
    """
    def __init__(self, full_name, description):
        self.full_name = full_name
        self.description = description
    def test(self, args):
        if "{}".format(self.full_name) in args:
            return True
        else:
            return False

class Option:
    """
    An argument to be passed to the program.
    Example: Option("name", "STRING", "Name of program")
    When the above example is used, --name=<string> corresponds to the program.
    Differing values for TYPE:
        TYPE="string": does not cast anything
        TYPE="int": casts to an integer
        TYPE="bool": casts to a bool
    """
    def __init__(self, name, TYPE, description):
        self.name = name
        self.description = description
    def test(self, arg):
        if arg.startswith("--{}=".format(self.name)):
            return True
        return False


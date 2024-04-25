class CopyError(ValueError):
    """
    Exception thrown when `var copy` fails.
    """
    def __init__(self, message="var.copy(): Cannot copy invalid variable"):
        super().__init__(message)

def get(var, fallback=""):
    """
    Returns the value of value `var`. If it does not exist, returns `fallback`.
    """
    vars = giveVars()
    try:
        return giveVars()[var]
    except KeyError:
        return fallback

def getint(var, fallback=0):
    """
    Returns an integer from a variable. Falls back to `fallback` if the variable is invalid or not an integer.
    """
    vars = giveVars()
    try:
        return int(giveVars[var])
    except ValueError:
        # Not an integer
        return fallback
    except KeyError:
        # Variable does not exist
        return fallback

def getbool(var, fallback=True):
    """
    Returns True if the value of `var` is either "true", "True", "yes", "Yes", or "1".
    Returns False for any other value, and fallback if `var` does not exist.
    """
    vars = giveVars()

    try:
        if giveVars()[var] in ["true", "True", "yes", "Yes", "1"]:
            return True
        else:
            return False
    except KeyError:
        return fallback

def set(var, val, fallback=""):
    """
    Sets variable `var` to `val`.
    """
    v = giveVars()
    v[var] = val


def list():
    """
    Prints out a list of variables.
    """
    var = giveVars()
    div()
    print("Variables")
    div()
    if not var:
        print("None set.")
    for v in var:
        print("{} = {}".format(v, var[v]))
    div()

def rm(name):
    """
    Deletes a variable. Returns True if the value was removed.
    """
    removed = False
    var = giveVars()
    try:
        del(giveVars()[name])
        removed = True
    except:
        pass
    return removed

def copy(from_var, to_var):
    """
    Copies the value of `from_var` to `to_var`. Raises a CopyError if `from_var` is an invalid variable name.
    """
    from_val = get(from_var, fallback=None)
    if not from_val:
        raise CopyError
    set(to_var, from_val)


def main(args):
    if args == ["set"]:
        div()
        print("var set <name> <value>.")
        div()
        print("Sets <name> to <value>.")
        div()
    elif args == ["get"]:
        div()
        print("var get <var>")
        div()
        print("Prints the value of <var>.")
        div()
    elif "get" in args and len(args) == 2:
        print(get(args[1]))
    elif args == ["list"]:
        list()
    elif "set" in args and len(args) == 3:
        set(args[1], args[2])
    elif args == ["rm"]:
        div()
        print("var rm <name>")
        div()
        print("Delete the variable.")
        div()
    elif "rm" in args and len(args) == 2:
        if not rm(args[1]):
            print("ERROR: Unable to remove.")
    elif args == ["copy"]:
        div()
        print("var copy <to_var> <from_var>")
        div()
        print("Copy a variable onto another variable.")
        print("E.G: `var copy foo bar` sets `bar` to the value of `foo`.")
        div()
    elif "copy" in args and len(args) == 3:
        args.remove("copy")
        try:
            copy(args[0], args[1])
        except CopyError:
            print("ERROR: Invalid variable '{}'.".format(args[0]))
    else:
        div()
        print("var [args]")
        div()
        print("Positional Arguments:")
        print("    set: sets a variable")
        print("    get: returns the value of a variable")
        print("    copy: copy a variable onto another variable")
        print("    rm: delete a variable")
        print("    list: lists all variables")
        div()

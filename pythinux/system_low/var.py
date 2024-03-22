def get(var, fallback=""):
    vars = giveVars()
    try:
        return giveVars()[var]
    except KeyError:
        return fallback

def getint(var, fallback=0):
    vars = giveVars()
    try:
        return int(giveVars[var])
    except ValueError:
        return fallback
    except KeyError:
        return fallback

def getbool(var, fallback=True):
    vars = giveVars()

    try:
        if giveVars()[var] in ["true", "True", "yes", "Yes", "1"]:
            return True
        else:
            return False
    except KeyError:
        return fallback

def set(var, val, fallback=""):
    v = giveVars()
    v[var] = val
    setVars(v)


def list():
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
    removed = False
    var = giveVars()
    try:
        del(giveVars()[name])
        removed = True
    except:
        pass
    setVars(var)
    return removed

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
    else:
        div()
        print("var [args]")
        div()
        print("Positional Arguments:")
        print("    set: sets a variable")
        print("    get: returns the value of a variable")
        print("    rm: delete a variable")
        print("    list: lists all variables")
        div()

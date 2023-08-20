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
    print(giveVars()[args[1]])
elif args == ["list"]:
    pprint(giveVars())
elif "set" in args and len(args) == 3:
    var = giveVars()
    var[args[1]] = args[2]
    setVars(var)
else:
    div()
    print("var [args]")
    div()
    print("Positional Arguments:")
    print("    set: sets a variable")
    print("    get: returns the value of a variable")
    print("    list: lists all variables")
    div()

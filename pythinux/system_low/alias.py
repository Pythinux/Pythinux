def main(args):
    arguments = args
    if arguments in [["list"], ["ls"]]:
        div()
        for item in aliases:
            print(f"{item} --> {aliases[item]}")
        if aliases == {}:
            print("No aliases loaded.")
        div()
    elif arguments == ["set"]:
        div()
        print("alias set <alias> <command>")
        div()
        print("Example:")
        print("alias set ? help")
        print("[Redirects \"?\" to \"help\"]")
        div()
    elif "set" in arguments and len(arguments) == 3:
        aliases[arguments[1]] = arguments[2]
        saveAliases(aliases)
    elif args == ["clear"]:
        saveAliases({})
        div()
        print("Cleared aliases.")
        div()
    elif arguments == ["remove"]:
        div()
        print("alias remove <alias>")
        div()
        print("Removes <alias> from aliases.")
        div()
    elif "remove" in arguments and len(arguments) == 2:
        try:
            aliases.pop(arguments[1])
            saveAliases(aliases)
        except:
            print(f"No alias found: {arguments[1]}")
    elif args == ["add"]:
        main(["set"])
    elif "add" in args and len(args) == 3:
        args.remove("add")
        main(["set"] + args)
    else:
        div()
        print("alias [args]")
        div()
        print("Arguments:")
        print("    list: lists all aliases")
        print("    set: set the value of an alias")
        print("    remove: removes an alias")
        print("    clear: removes all aliases")
        div()

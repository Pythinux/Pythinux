libargs = load_program("libargs", currentUser, libMode=True)

parser = libargs.ArgumentParser("alias", description="Handles aliases")
subs = parser.add_subparsers(dest="cmd", help="Sub-command help")

parser_list = subs.add_parser("list", help="Lists aliases")

parser_set = subs.add_parser("set", help="Sets an alias")
parser_set.add_argument("alias", help="Alias name")
parser_set.add_argument("command", help="Command to execute")


parser_set = subs.add_parser("add", help="Sets an alias")
parser_set.add_argument("alias", help="Alias name")
parser_set.add_argument("command", help="Command to execute")

parser_remove = subs.add_parser("remove", help="Removes an alias")
parser_remove.add_argument("alias", help="Alias to remove")

parser_clear = subs.add_parser("clear", help="clears all aliases")
parser_clear.add_argument("-y", action="store_true", help="Confirm choice")

def listAliases():
    div()
    for item in aliases:
        print("{} --> {}".format(item, aliases[item]))
    div()

def setAlias(alias, command):
    assertTrue(isinstance(alias, str), "Invalid string")
    assertTrue(isinstance(command, str), "Invalid string")
    aliases[alias] = command
    saveAliases(aliases)

def removeAlias(alias):
    assertTrue(isinstance(alias, str), "Invalid string")
    aliases.pop(alias)
    saveAliases(aliases)

def clearAliases():
    saveAliases({})

def main(args):
    args = parser.parse_args(args)
    if args.cmd == "list":
        listAliases()
    elif args.cmd in ["add", "set"]:
        setAlias(args.alias, args.command)
    elif args.cmd == "remove":
        removeAlias(args.alias)
    elif args.cmd == "clear":
        if args.y:
            clearAliases()
        else:
            print("To confirm this, run 'alias clear -y'.")
    else:
        parser.print_help()

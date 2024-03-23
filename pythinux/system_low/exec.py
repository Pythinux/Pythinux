def exec(command):
    runCommand(currentUser, command)

def main(args):
    if args:
        exec(" ".join(args))
    else:
        div()
        print("exec <comamnd>")
        div()
        print("Run a command.")
        print("Can be useful if your shell blocks certain commands.")
        div()

def terminal():
    while True:
        cmd = input("bterm $")
        if cmd in ["quit", "exit"]:
            return
        print(runCommand(currentUser, cmd))
def main(args):
    div()
    print("Basic Terminal Emulator")
    div()
    print("Enter \"exit\" or \"quit\" to quit the terminal.")
    div()
    terminal()

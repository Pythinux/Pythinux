def terminal(x=""):
    if x not in ["exit","quit"]:
        print(main(currentUser,x))
        terminal(input("basic-terminal $"))
def main(args):
    div()
    print("Basic Terminal Emulator")
    div()
    print("Enter \"exit\" or \"quit\" to quit the terminal.")
    div()
    terminal()

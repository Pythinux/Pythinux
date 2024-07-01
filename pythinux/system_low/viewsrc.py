which = load_program("which", currentUser, libMode=True)

def view(program):
    """
    Returns the source code of a named program as a string.
    """
    program = which.which([program])[0]
    with file.open(program, currentUser) as f:
        return f.read()


def main(args):
    if args:
        for arg in args:
            code = view(arg)
            print(code if code else "ERROR: Invalid program name.")
    else:
        div()
        print("viewsrc [list of programs]")
        div()
        print("Display the src code of a program.")
        div()

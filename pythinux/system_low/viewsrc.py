which = load_program("which", currentUser, libMode=True)

def view(program):
    program = which.which([program])[0]
    with open(program) as f:
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

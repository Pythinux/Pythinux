import traceback
help = load_program("help", currentUser, libMode=True)
shell = load_program("shell", currentUser, libMode=True)
libargs = load_program("libargs", currentUser, libMode=True)
var = load_program("var", currentUser, libMode=True)

module = type(__builtins__)

def blank():
    pass

def main(args):
    for program in help.help():
        try:
            mod = load_program(program, currentUser, libMode=True)
            if "main" not in dir(mod):
                print("ERROR: {} has no main()".format(program))
        except:
            pass

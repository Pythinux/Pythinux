import code
def main(args):
    code.interact(local=globals() if "--global" in args else locals(),banner="Python Interpreter: press Ctrl+D to exit",exitmsg="Exit Python interpreter.")

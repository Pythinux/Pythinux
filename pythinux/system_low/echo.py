def echo(args):
    print(" ".join(args))

def main(args):
    if args:
        echo(args)
    else:
        div()
        print("Echo <text>")
        div()
        print("Echoes <text> to the terminal.")
        div()

def cat(filename):
    with open(filename) as f:
        print(f.read())
def main(args):
    if args:
        for arg in args:
            cat(arg)
    else:
        div()
        print("cat [files]")
        div()
        print("Prints the contents of a file.")
        div()

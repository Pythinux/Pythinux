def cat(filename, user=None):
    with file.open(filename, user if user else currentUser) as f:
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

if args:
    args = " ".join(args)
    with open(args) as f:
        print(f.read())
else:
    div()
    print("cat <file>")
    div()
    print("Prints the contents of <file>.")
    div()

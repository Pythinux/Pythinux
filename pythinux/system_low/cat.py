if args:
    for arg in args:
        with open(arg) as f:
            print(f.read())
else:
    div()
    print("cat [files]")
    div()
    print("Prints the contents of a file.")
    div()

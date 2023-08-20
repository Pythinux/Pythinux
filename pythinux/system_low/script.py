if args:
    with open(" ".join(args)) as f:
        run_script(f,currentUser)
else:
    div()
    print("script </path/to/file>")
    div()
    print("Reads the contents of <file> and runs them as a script.")
    div()

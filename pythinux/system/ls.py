if args == ["--help"]:
    div()
    print("ls: lists contents of /")
    print("ls <directpry>: lists contents of <directory>")
    div()
elif args:
    div()
    print(" ".join(os.listdir(" ".join(args))))
    div()
else:
    div()
    print(" ".join(os.listdir(cdir)))
    div()

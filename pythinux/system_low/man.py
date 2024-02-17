def dirTree(path):
    if not os.path.isdir(path):
        print("Error: invalid path.")
    else:
        div()
        for root, dirs, files in os.walk(path):
            if root.startswith("man/"):
                root=root[3:]
            elif root.startswith("man"):
                root=root[4:]
            if root.startswith("/"):
                root=root[1:]
            for file in files:
                print(os.path.join(root,file))
        div()


if args == []:
    main(currentUser,"man man")
elif args == ["/"]:
    dirTree("man")
else:
    manual = "man/" + " ".join(args)
    if os.path.isfile(manual):
        with open(manual) as f:
            cls()
            print(f.read())
            br()
            cls()
    else:
        print("ERROR: Invalid manual.")

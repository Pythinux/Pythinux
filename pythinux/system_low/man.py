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

def man(manual):
    if os.path.isfile(manual):
        with open(manual) as f:
            cls()
            div()
            print(f.read())
            br()
            cls()

def main(args):
    if args == []:
        runCommand(currentUser,"man man")
    elif args == ["/"]:
        dirTree("man")
    else:
        manual = "man/" + " ".join(args)
        man(manual)
        else:
            print("ERROR: Invalid manual.")

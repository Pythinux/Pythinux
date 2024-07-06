def dirTree():
    manuals = []
    path = "man/"
    for root, dirs, files in os.walk(path):
        for file in files:
            manuals.append(file)
    return files
def main(args):
    if args == ["/"]:
        div()
        print("\n".join(sorted(dirTree())))
        div()
    else:
        if args:
            manual = "man/" + " ".join(args)
        else:
            manual = "man/man"
        try:
            with file.open(manual, currentUser) as f:
                cls()
                div()
                print(f.read())
                br()
                cls()
        except FileNotFoundError:
            print("ERROR: Manual `{}` is not valid.".format(manual))

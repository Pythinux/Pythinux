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
        if os.path.isfile(manual):
            with open(manual) as f:
                cls()
                div()
                print(f.read())
                br()
                cls()
        else:
            print("ERROR: Manual `{}` is not valid.".format(manual))

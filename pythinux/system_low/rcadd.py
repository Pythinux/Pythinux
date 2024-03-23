def add(command):
    """
    Adds `command` to `~/shellrc.xx`.
    """
    with open(file.evalDir("~/shellrc.xx", currentUser), "a") as f:
        f.write("\n{}".format(command))
def main(args):
    if args:
        add(" ".join(args))
    else:
        div()
        print("rcadd [command]")
        div()
        print("Adds a command to ~/shellrc.xx")
        div()

def add(command, user=None):
    assertTrue(isinstance(command, str))
    assertTrue(type(user) in [type(None), User])
    """
    Adds `command` to `~/shellrc.xx`.
    """
    with file.open("~/shellrc.xx", user if user else currentUser, "a") as f:
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

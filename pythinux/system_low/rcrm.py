def remove(command, user=None):
    assertTrue(isinstance(command, str))
    assertTrue(type(user) in [type(None), User])
    with file.open("~/shellrc.xx", user if user else currentUser) as f:
        contents = f.read().replace(command, "")
        old = f.read()
    with file.open("~/shellrc.xx", user, "w") as f:
        f.write(contents)
    return old

def main(args):
    if args:
        remove(" ".join(args), currentUser)
    else:
        div()
        print("rcrm [command]")
        div()
        print("Remove a command from your shellrc file.")
        div()

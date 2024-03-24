def remove(command, user):
    with file.open("~/shellrc.xx", user) as f:
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

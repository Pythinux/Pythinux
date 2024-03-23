def view(user):
    with open(file.evalDir("~/shellrc.xx", user)) as f:
        return f.read()

def main(args):
    print(view(currentUser))

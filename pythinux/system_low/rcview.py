def view(user):
    assertTrue(isinstance(user, User))
    with file.open("~/shellrc.xx", user) as f:
        return f.read()

def main(args):
    print(view(currentUser))

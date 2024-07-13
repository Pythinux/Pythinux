def cd(directory):
    assertTrue(isinstance(directory, str))
    file.changeDirectory(directory, currentUser)

def main(args):
    if args:
        cd(" ".join(args))
    else:
        div()
        print("cd <directory>")
        div()
        print("Change working directory.")
        div()

def cd(directory):
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

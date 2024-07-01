def main(args):
    if args == ["--help"]:
        div()
        print("ls: lists contents of /")
        print("ls <directpry>: lists contents of <directory>")
        div()
    else:
        directory = file.evalDir(" ".join(args), currentUser) if args else file.evalDir(CURRDIR, currentUser)
        div()
        print("\n".join(os.listdir(directory)))
        div()

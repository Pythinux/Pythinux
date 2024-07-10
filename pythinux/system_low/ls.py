libargs = load_program("libargs", currentUser, libMode=True)

parser = libargs.ArgumentParser("ls", description="Lists contents of a directory")
parser.add_argument("directory", help="Directory to list contents of", nargs="?")
parser.add_argument("--version", "-V", help="Displays version info", action="store_true")

def getFileList(directory, user=None):
    return os.listdir(file.evalDir(directory, user if user else currentUser))

def formatDirectory(files):
    div()
    for file in files:
        print(file)
    div()

def main(args):
    args = parser.parse_args(args)
    if args.version:
        print("ls 2.0")
        return
    formatDirectory(getFileList(args.directory if args.directory else "."))

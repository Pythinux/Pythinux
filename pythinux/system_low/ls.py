libargs = load_program("libargs", currentUser, libMode=True)

parser = libargs.ArgumentParser("ls", description="Lists contents of a directory")
parser.add_argument("directory", help="Directory to list contents of", nargs="?")

def getFileList(directory, user=None):
    assertTrue(isinstance(directory, str))
    assertTrue(type(user) in [type(None), User])
    return os.listdir(file.evalDir(directory, user if user else currentUser))

def formatDirectory(files):
    assertTrue(isinstance(files, list) and all(isinstance(elem, str) for elem in files))
    div()
    for file in files:
        print(file)
    div()

def main(args):
    args = parser.parse_args(args)
    formatDirectory(getFileList(args.directory if args.directory else "."))

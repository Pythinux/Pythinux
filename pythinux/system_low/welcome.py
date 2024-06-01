curl = load_program("curl", currentUser, libMode=True)

def welcome():
    return curl.curl("https://codeberg.org/Pythinux/Pythinux/raw/branch/main/welcome.txt")
def main(args):
    print(welcome())

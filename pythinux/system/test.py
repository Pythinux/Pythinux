import traceback

libsemver = load_program("libsemver", currentUser, libMode=True)

def main(args):
    a, b, c, = "1.0.0", "1.0.0-1", "1.0.0-2"
    # print(libsemver.check(a))
    # print(libsemver.check(b))
    # print(libsemver.check(c))
    print(libsemver.compare(b,c))
    print(libsemver.compare(c,b))

import os

DIRS = ["system", "system_low", "app", "app_high", "system_high"]

def which(args):
    foundFiles = []
    for arg in args:
        found = False
        for DIR in DIRS:
            FILE = "{}/{}.py".format(DIR, arg)
            if os.path.isfile(FILE):
                foundFiles.append(FILE)
                found = True
                break
        if not found:
            foundFiles.append("N/A")
    return foundFiles
def main(args):
    if args:
        for x in which(args):
            print(x)
    else:
        div()
        print("which [list of programs]")
        div()
        print("Finds the path of a program.")
        div()

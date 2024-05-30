import os
def main(args):
    if args:
        args = " ".join(args)
        os.mkdir(args)
    else:
        div()
        print("mkdir [directory]")
        div()
        print("Creates [directory] if it does not exist.")
        div()

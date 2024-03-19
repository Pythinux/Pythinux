import os
def cmd(cmd):
    os.system(cmd)
def main(args):    
    if args:
        cmd(" ".join(args))
    else:
        div()
        print("cmd <command>")
        div()
        print("Execute a command on your base system.")
        div()

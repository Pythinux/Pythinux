import os
import argparse

parser = argparse.ArgumentParser("cmd", description="Run a command on the base system", epilog="(c) 2024 Pythinux Team")
parser.add_argument("command", nargs="+", help="The command to run")

def cmd(cmd):
    """
    Runs a command on the host shell.
    """
    assert(isinstance(cmd, str))
    os.system(cmd)
def main(args):    
    if args:
        args = parser.parse_args(args)
        cmd(" ".join(args.command))
    else:
        parser.print_help()

import os
import importlib
import zipfile
import traceback
import shutil
import sys

def installd(file):
    pass

def main(args):
    if args:
        installd(" ".join(args))
    else:
        div()
        print("installd /path/to/program.szip4")
        div()
        print("Install an SZIP4 package.")
        div()

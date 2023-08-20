#!/usr/bin/python
import time
import os
from pythinux import *
import pythinux

os.chdir("pythinux")
global currentUser, currentGroup, userList, startTime
startTime = time.time()
currentGroup = Group("unit", True, True, True, True)
p = hashString("unittest")
currentUser = User(currentGroup, "test", p)
userList = UserList()
userList.add(currentUser)
installd = load_program("installd", currentUser)


class Unit(Base):
    def __init__(self, name, command):
        self.name = name
        self.command = command

    def execute(self):
        print(self.command)


class CommandUnit(Unit):
    def execute(self):
        o = pythinux.load_program(self.command, currentUser)
        if o:
            print(o)


class OSUnit(Unit):
    def execute(self):
        os.system(self.command)


class FunctionUnit(Unit):
    def execute(self):
        self.command()


i = 1


def function():
    print(os.getcwd())


def makeUser():
    g = Group("testgroup")
    u = User(g, "testuser")
    return u


def objectToDict():
    obj = makeUser()
    return obj_to_dict(obj)


def mkPPrint():
    g = makeUser()
    pprint(g)


def loadAllPrograms():
    i = 1
    c = list_loadable_programs(currentUser)
    for item in c:
        print("    ({}/{}) {}".format(i, len(c), item))
        main(currentUser, item)
        i += 1


def documentPy():
    os.chdir("..")
    os.system("pydoc pythinux | grep ''")
    os.chdir("pythinux")


if __name__ == "__main__":
    units = [
        FunctionUnit("Copy Module", lambda: copy(FunctionUnit)),
        FunctionUnit("Print Current Directory", function),
        # Unit("Test", "Testing..."),
        # CommandUnit("Install StartPKG","pkm install -y startpkg")
        # FunctionUnit("Run All Programs",loadAllPrograms)
        FunctionUnit("Create Module", lambda: createModule("unit_test")),
        OSUnit("Run Pydoc", "pydoc pythinux > /dev/null"),
        FunctionUnit("Create User", makeUser),
        FunctionUnit("Load user list", loadUserList),
        FunctionUnit("Load group list", loadGroupList),
        FunctionUnit("Convert Object to Dictionary", objectToDict),
        FunctionUnit("pprint", mkPPrint),
        FunctionUnit(
            "Loadable Programs", lambda: print(
                list_loadable_programs(currentUser
                                       ))
        ),
        OSUnit(
            "Lint Test [unittest]",
            "flake8 ../unittest.py --ignore F405,F403"
        ),
        # OSUnit("Lint Test [pythinux]", "flake8 ../pythinux.py"),
        OSUnit("Lint Test [resetInstall]", "flake8 ../resetinstall.py"),
        # FunctionUnit("PyDoc",documentPy),
    ]
    print("Begin unit tests.")
    for unit in units:
        print("[{}] [{}/{}] {}".format(
            round((time.time() - startTime), 5), i, len(units), unit.name))
        unit.execute()
        i += 1
    print("All unit tests complete.")

"""
██████╗ ██╗   ██╗████████╗██╗  ██╗██╗███╗   ██╗██╗   ██╗██╗  ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██║████╗  ██║██║   ██║╚██╗██╔╝
██████╔╝ ╚████╔╝    ██║   ███████║██║██╔██╗ ██║██║   ██║ ╚███╔╝ 
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║██║╚██╗██║██║   ██║ ██╔██╗ 
██║        ██║      ██║   ██║  ██║██║██║ ╚████║╚██████╔╝██╔╝ ██╗
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝

Copyright (C) 2024 Pythinux Team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import traceback
import contextlib
import io


var = load_program("var", currentUser, libMode=True)
pwd = load_program("pwd", currentUser, libMode=True)

class ShellError(Exception):
    def __str__(self, *args, **kwargs):
        return "ERROR: {}".format(self.args[0])

def pipe(value):
    """
    Accepts a piped shell script.
    """
    assertTrue(isinstance(value, str))

    with file.open("/tmp/shell.xx", currentUser, "w") as f:
        f.write(value)
    runScript(currentUser, "/tmp/shell.xx")

def fixDir(user):
    assertTrue(isinstance(user, User), "Not a user object")

    os.chdir(file.evalDir(pwd.pwd(), user))

def splitList(inputList, separator):
    """
    Splits a list into sublists with a given separator.
    """
    result = []
    sublist = []
    for item in inputList:
        if item == separator:
            result.append(sublist)
            sublist = []
        else:
            sublist.append(item)
    result.append(sublist)
    return result

def getCommandOutput(user, cmd, **kwargs):
    """
    Run a command silently and return its output as a string.
    """
    with contextlib.redirect_stdout(io.StringIO()) as f:
        run(user, cmd, **kwargs)
    return f.getvalue().rstrip("\n")

def pipeCommandOutput(user, cmd, second_cmd, **kwargs):
    """
    Pipes the output of one command into another.
    """
    assertTrue(isinstance(user, User))
    assertTrue(isinstance(cmd, str))
    assertTrue(isinstance(second_cmd, str))

    output = getCommandOutput(user, cmd, **kwargs)
    program = load_program(second_cmd, user, libMode=True, **kwargs)
    if not program:
        raise ShellError("This program is invalid.")
    if not "pipe" in dir(program):
        raise ShellError("This program cannot accept piped data.")
    program.pipe(output)

def run(user:pythinux.User, cmd, lastCommand="", shell="shell"):
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(cmd, str), "Command must be a string")
    assertTrue(isinstance(lastCommand, str), "Command must be a string")
    assertTrue(isinstance(shell, str), "Shell name must be a string")

    def handleRedirection(cmd_args):
        filename = cmd_args[-1]
        run = " ".join(cmd_args[:-2])
        with file.open(filename, currentUser, "w") as f:
            f.write(getCommandOutput(currentUser, run))

    def handlePiping(cmd_args):
        cmds = splitList(cmd_args, "|")
        cmds = [" ".join(x) for x in cmds]
        assertTrue(len(cmds) == 2, "Cannot pipe more than once", PythinuxError)
        pipeCommandOutput(currentUser, cmds[0], cmds[1])

    lastCommandArgs = " ".join(lastCommand.split(" ")[1:])
    if "!!" in cmd:
        cmd = cmd.replace("!!", lastCommand)
    if "!" in cmd:
        cmd = cmd.replace("!", lastCommandArgs)

    cmd_args = cmd.split(" ")
    if ">" in cmd_args and cmd_args[-2] == ">":
        try:
            handleRedirection(cmd_args)
        except ShellError as e:
            print(e)
        except Exception as e:
            print(traceback.format_exc())
        return
    if "|" in cmd_args:
        try:
            handlePiping(cmd_args)
        except ShellError as e:
            print(e)
        except Exception as e:
            print(traceback.format_exc())
        return


    if cmd == "":
        pass
    elif cmd in ["quit", "exit"] and not var.getbool("SHELL_ALLOW_EXIT", True):
        pass
    elif cmd in ["quit", "exit"]:
        return "EXIT_STATE"
    elif cmd in ["logoff", "logout"] and not var.getbool("SHELL_ALLOW_LOGOFF", True):
        pass
    elif cmd in ["logoff", "logout"]:
        loginScreen()
    else:
        try:
            runCommand(user, cmd, shell=shell)
        except ShellError as e:
            print(e)
        except SystemExit:
            pass
        except Exception as e:
            print(traceback.format_exc())


def init(user: User):
    assertTrue(isinstance(user, User), "Not a user object")

    fileName = "~/shellrc.xx"
    runScript(user, fileName)
    file.changeDirectory("~", user)

def terminal(user: User, lastCommand=""):
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(lastCommand, str), "Command must be a string")

    try:
        cmd = input("[{}@{} {}] $".format(user.group.name, user.username, pwd.pwd()))
    except KeyboardInterrupt:
        print()
        terminal(user, lastCommand)
    try:
        fixDir(user)
        output = run(user, cmd, lastCommand)
        fixDir(user)
        if output == "EXIT_STATE":
            return
    except KeyboardInterrupt:
        pass
    if ["!"] in cmd.split(" "):
        terminal(user, lastCommand)
    else:
        terminal(user, str(cmd))

def runScript(user: pythinux.User, filename):
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(filename, str), "File name must be a string")

    if not verifyUser(user):
        raise PythinuxError("User instance provided is not of the expected User class")
    with file.open(filename, user) as f:
        for cmd in [x for x in f.read().split("\n") if not x.startswith(";")]:
            run(user, cmd, "script")

def main(args):
    if args:
        for arg in args:
            runScript(currentUser, arg)
    else:
        div()
        print("shell <script_name.xx>")
        div()
        print("Runs a shell script.")
        div()

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

def fixDir(user):
    assertTrue(isinstance(user, User), "Not a user object")

    os.chdir(file.evalDir(pwd.pwd(), user))

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
    output = getCommandOutput(user, cmd, **kwargs)
    program = load_program(second_cmd, user, libMode=True, **kwargs)
    if not program:
        raise PythinuxError("Invalid program")
    if not "pipe" in dir(program):
        raise PythinuxError("Unsupported program")
    program.pipe(output)

def run(user:pythinux.User, cmd, lastCommand="", shell="shell"):
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(cmd, str), "Command must be a string")
    assertTrue(isinstance(lastCommand, str), "Command must be a string")
    assertTrue(isinstance(shell, str), "Shell name must be a string")

    lastCommandArgs = " ".join(lastCommand.split(" ")[1:])
    if "!!" in cmd:
        cmd = cmd.replace("!!", lastCommand)
    if "!" in cmd:
        cmd = cmd.replace("!", lastCommandArgs)

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

#/!usr/bin/env python

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


import os
import pickle
import sys
import hashlib
import traceback
import inspect
import re
import platform
import shutil
import importlib.util
import threading
import ast
import copy as cp
import asyncio
import io
from getpass import getpass
import warnings
import configparser
import time
import contextlib
import string
import random
import secrets

try:
    import pty
    unixMode = True
except:
    unixMode = False

osName = "Pythinux"
version = [3, 2 ,0]
var = {}
aliases = {}
EVALHIST = []

# Kernel parameters - designed to be edited with a text editor

## Security
KPARAM_USE_MODULE_WRAPPER = True # Fix for PSA-0004
KPARAM_ESCALATION_PROTECTION = True # Protects against privilege escalation
KPARAM_ARTIFICIAL_DECRYPT_TIME = False # If True, verifyHash() will wait a set amount of seconds before trying to decrypt
KPARAM_INT_ARTIFICIAL_DECRYPT_TIME = 0.5 # The amount of time KPARAM_ARTIFICIAL_DECRYPT_TIME waits for

## Debugging
KPARAM_DEBUGGING_VERIFYUSER = False # Shows debugging info for verifyUser()
KPARAM_DEBUGGING_VERIFYUSER_EXTENDED = False # Shows what group verifyUser() expects (very messy output)
KPARAM_DEBUGGING_VERIFYHASH = False # Display a message every time verifyHash() is called
KPARAM_DISABLE_CLS = False # If true, the cls() function is disabled system-wide
KPARAM_DEBUGGING_LIMITED_OPEN = False # If true, limitedOpenFile() will print values of all files passed to it
KPARAM_DEBUGGING_LOAD_PROGRAM = False # If True, debug info will show every time loadProgramBasBasee() is called

## Feature testing
KPARAM_USE_LIMITED_OPEN = True # Uses limitedOpenFile() for file.open()
KPARAM_DEPRECATE_OPEN = True # If True, open() raises a DeprecationWarning
KPARAM_REAL_DIRECTORY = True # If enabled, Real Directory Support is enabled

# Files that cannot be opened

# By all users
BLOCKED_FILES = [
    "/config/debuggers"
]

# By unprivileged users
USER_BLOCKED_FILES = BLOCKED_FILES + [
    "/config/users.ini",
    "/config/groups.ini",
    "/config/pkmdata.ini",

]

# System programs with ability to debug
SYSTEM_DEBUGGERS = [
    "debugmgr",
]

with open("default.xx") as f:
    DEFAULT_SHELL_SCRIPT = f.read()


def assertTrue(condition, message=None, error=AssertionError):
    """
    Checks if `condition` is True. If it isn't, it raises an AssertionError.
    """
    if not condition:
        raise error(message) if message else error

class PythinuxError(Exception):
    """
    Generic exception raised by the kernel (and system programs) when an issue occurs.
    """

    def __init__(self, text):
        self.text = str(text)

    def __str__(self):
        return self.text

class DevRandomStringIO(io.StringIO):
    """
    Implementation of /dev/random as a StringIO.
    """
    def __init__(self, length=1024):
        self.length = length
        random_data = self._generate_random_string(self.length)
        super().__init__(random_data)

    def _generate_random_string(self, length):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    def read(self, size=-1):
        if size == -1:
            size = self.length
        return super().read(size)

class DevURandomStringIO(DevRandomStringIO):
    def _generate_random_string(self, length):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(length))

def loadGroupList():
    try:
        with open("config/usergroups.cfg", "rb") as f:
            return pickle.load(f)
    except Exception:
        g = GroupList()
        saveGroupList(g)
        return g


def saveGroupList(groupList):
    if isinstance(groupList, GroupList):
        with open("config/usergroups.cfg", "wb") as f:
            pickle.dump(groupList, f)
    else:
        raise PythinuxError("Invalid grouplist to save.")


def fixDirectories(returnMode=False):
    """
    Reconstructs the blank directories if they do not exist,
    because git doesn't count directories as files.
    """
    dirList = [
        "app",
        "app_high",
        "config",
        "home",
        "lib",
        "lib_high",
        "log",
        "share",
        "share/pkm",
        "share/pkm/programs",
        "share/pkm/script",
        "share/pkm/script/remove",
        "share/pkm/script/update",
        "tmp",
    ]
    if returnMode:
        return dirList
    for item in dirList:
        if not os.path.isdir(item):
            os.mkdir(item)


def verifyUser(user):
    """
    Returns True if the user is not a fake instance of User.
    """
    assertTrue(isinstance(user, User), "Did not specify an instance of User", PythinuxError)
    # 'Equal To' Check 
    expectedUser = loadUserList().byName(user.username)
    if not expectedUser:
        if KPARAM_DEBUGGING_VERIFYUSER:
            print("DEBUG: Could not find expected group")
        return False

    if KPARAM_DEBUGGING_VERIFYUSER_EXTENDED:
        print("DEBUG: Detected group '{}'".format(expectedUser.group.name))

    
    # Permissions Check
    if (
        user.group.canApp != expectedUser.group.canApp
        or user.group.canAppHigh != expectedUser.group.canAppHigh
        or user.group.canSys != expectedUser.group.canSys
        or user.group.locked != expectedUser.group.locked
    ):
        if KPARAM_DEBUGGING_VERIFYUSER:
            print("DEBUG: Group check failed")
        return False
    # Memory address check
    return id(type(user)) in [id(User), id(CurrentUser)]


def giveVars():
    """
    Returns the list of variables loaded by the program.
    """
    return var


def createModule(moduleName):
    """
    Creates a module object, which not normally creatable.
    """
    return type(os)(moduleName)


def silent(function):
    """
    Runs some code without outputting anything to the terminal.
    Args:
        function: a callable object.
    """
    assertTrue(callable(function), "silent(): Function is not callable")
    with contextlib.redirect_stdout(io.StringIO())  as f:
        x = function()
    return x


class FileError(Exception):
    """
    Generic exception for indicating an issue with opening or parsing a file.
    Args:
    text: what to display to the user.
    """

    def __init__(self, text):
        self.text = text

    def write(self, text):
        return text


def joinIterable(string, iterable):
    """
    Joins a string and an iterable together.
    Args:
    string: The initial string to join to
    iterable: an iterable object to join
    Returns:
    string + every item in iterable
    """
    return string.join([str(x) for x in iterable])


def attachDebugger(globals):
    assertTrue(isinstance(globals, dict), "Globals is not a dictionary")
    import code
    code.InteractiveConsole(locals=globals)


def doCalc(text):
    """
    A fully safe (but very restricted) version of eval().
    Undergoes HEAVY sanitisation before execution.
    """
    assertTrue(isinstance(text, str), "Cannot perform calculations on a non-integer")
    allowed_nodes = (ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Constant)
    allowed_operators = (ast.Add, ast.Sub, ast.Mult, ast.Div)
    allowed_names = {"math"}

    try:
        wrapped_text = f"result = {text.strip()}"
        module = ast.parse(wrapped_text, mode="exec")
        expr = module.body[0].value
        for node in ast.walk(expr):
            if not isinstance(node, allowed_nodes):
                raise ValueError("Invalid expression")
            if isinstance(node, ast.Name) and node.id not in allowed_names:
                raise ValueError("Invalid expression")
            if isinstance(node, ast.BinOp) and not isinstance(
                node.op, allowed_operators
            ):
                raise ValueError("Invalid expression: {}".format(text))
        namespace = {}
        exec(compile(module, filename="<ast>", mode="exec"), namespace)
        result = namespace["result"]

        return result

    except (SyntaxError, ValueError) as e:
        return f"Error: {str(e)}"


class Base:
    """
    Base class used by all classes.
    This class is used as a base for other classes exclusively,
    and is not called directly.
    """

    __slots__ = ["__weakref__"]

    def __str__(self):
        """
        Printing an object will return the object passed
        through pprint_dict(obj_to_dict()).
        """
        return pprint_dict(obj_to_dict(self))

    def __iter__(self):
        """
        Iterating through a Base object iterates through the keys and not the
        values.
        """
        return iter(sorted(self.__dict__.keys()))

    def __len__(self):
        """
        Runing len() for a Base object returns the amount of attributes it has.
        """
        return len(dir(self))


class TrueValue(Base):
    """
    Serves the same purpose as bool, but because True and False are different classes, they cannot be edited.
    """
    def __bool__(self):
        return True


class FalseValue(Base):
    """
    Serves the same purpose as bool, but because True and False are different classes, they cannot be edited.
    """
    def __bool__(self):
        return False


class SudoError(Exception):
    """
    Generic exception for issues with sudo privileges.
    """

    def __str__(self):
        return "Insufficient privileges to execute action."


class LOGOFFEVENT:
    """
    This class(not an instance of it) is returned by main() when
    the user uses the "logoff" command.
    """


def hashString(plaintext, salt=None):
    assertTrue(isinstance(plaintext, str), "Cannot hash a non-string")
    """
    Hashing algorithm used by Pythinux.
    Args:
        plaintext: a string.
        salt: an optional salt, usually a bytes-like object. If none is
        provided, a random one is generated.
    Returns:
        salted_hash: The final hash. The last 16 characters is the salt,
        required to verify the hash.
    The verifyHash function is used to authenticate hashes.
    """
    if salt is None:
        salt = os.urandom(16).hex()

    salted_string = f"{plaintext}{salt}"
    hashed_string = hashlib.sha256(salted_string.encode()).hexdigest()
    salted_hash = f"{hashed_string}{salt}"
    return salted_hash


def doNothing(obj):
    """
    Returns obj.
    Used to prevent linter programs from complaining about "unused" objects.
    """
    warnings.warn("doNothing will be removed in Pythinux 3.3", DeprecationWarning)
    return obj


class Group(Base):
    """
    User groups with custom permissions.
    """

    def __init__(
        self,
        name,
        canApp=False,
        canAppHigh=False,
        canSys=False,
        canSudo=False,
        locked=False,
    ):
        """
        Defines nanme and permissions of the Group.
        name: name of group. Set to all-lowercase.
        canApp: Boolean. Defines whether or not the user can access apps.
        canAppHigh: Boolean. Defines whether or not the user can access
            high-access apps.
        canSys: Boolean. Defines whether or not the user can access system
            apps in the "system" directory.
        canSudo: Boolean. Determines whether or not the user can use `sudo`.
        """
        assertTrue(isinstance(name, str), "Group name must be a string")
        assertTrue(isinstance(canApp, bool), "Group attributes must be boolean")
        assertTrue(isinstance(canAppHigh, bool), "Group attributes must be boolean")
        assertTrue(isinstance(canSys, bool), "Group attributes must be boolean")
        assertTrue(isinstance(canSudo, bool), "Group attributes must be boolean")
        assertTrue(isinstance(locked, bool), "Group attributes must be boolean")
        self.name = name.lower()
        self.canApp = canApp
        self.canAppHigh = canAppHigh
        self.canSys = canSys
        self.canSudo = canSudo
        self.locked = locked

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False
        return (
            self.name == other.name
            and self.canAppHigh == other.canAppHigh
            and self.canApp == other.canApp
            and self.canSys == other.canSys
            and self.canSudo == other.canSudo
            and self.locked == other.locked
        )


class GroupList(Base):
    """
    GroupList class for use in saveGroupList()/loadGroupList().
    """

    def __init__(self):
        self.groups = [
            Group("guest"),
            Group("user", True, canSudo=True, locked=True),
            Group("root", True, True, True, locked=True),
        ]

    def add(self, group):
        """
        Adds a group to the GroupList.
        Args:
        * group: a Group instance.
        """
        assertTrue(isinstance(group, Group), "Can only add a Group object to the group list")
        self.groups.append(group)

    def remove(self, group):
        if group.locked:
            raise PythinuxError("Cannot remove a built-in group.")
        else:
            self.groups.remove(group)

    def list(self):
        """
        Returns the list of groups.
        """
        return copy(self.groups)

    def byName(self, name):
        """
        Returns the first instance of a group based on its name.
        """
        assertTrue(isinstance(name, str), "Group names can only be strings")
        for item in self.groups:
            if item.name == name:
                return item

    def __len__(self):
        return len(self.groups)


class User(Base):
    """
    User class used by Pythinux.
    See __init__() for how to create User objects properly.
    """

    def __init__(self, group, username, password="", locked=False, disabled=False):
        """
        Constructor for User class.
        Args:
            group: a Group object.
            username: string, the username for the user.
            password: string passed through hashString() (Note: you MUST
            pass it through hashString().
                If no password is given, the password is blank.
                (the hash obviously still exists. pydoc represents the
                output of hashString("") as the default password.)
        """
        assertTrue(isinstance(group, Group), "User's group must be a Group object")
        assertTrue(isinstance(username, str), "User's username must be a string")
        assertTrue(isinstance(password, str), "User's password must be a string")
        assertTrue(isinstance(locked, bool), "User attributes must be boolean")
        assertTrue(isinstance(disabled, bool), "User attributes must be boolean")
        self.group = group
        self.username = username
        self.password = password
        self.locked = locked
        self.disabled = disabled

    def check(self, username, password=hashString("")):
        """
        Function for checking whether a User class and passed details match.
        Args:
            username: string
            password: string
        Returns:
            bool depending on whether or not the supplied details match up
            with the User object's properties.
        """
        if username == self.username and verifyHash(password, self.password):
            return True
        return False

    def admin(self):
        warnings.warn("user.admin() is deprecated, use user.group.canAppHigh instead", DeprecationWarning)
        return self.group.canAppHigh

    def USERTYPE(self):
        """
        Returns the name of the user's group.
        """
        return self.group.name

    def serialise(self):
        return {
            "username": self.username,
            "password": self.password,
            "group": self.group.name,
            "disabled": self.disabled,
            "locked": self.locked,
        }

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            other.username == self.username
            and other.password == self.password
            and other.group == self.group
        )


class UserList(Base):
    def __init__(self):
        self.users = []
        self.append = self.add

    def add(self, user):
        """
        Adds a user to the user list.
        """
        assertTrue(isinstance(user, User), "Can only add User objects to the user list")
        self.users.append(user)

    def byName(self, name):
        """
        Returns the first instance of
        a user in the userlist with the same name.
        """
        assertTrue(isinstance(name, str), "Usernames can only be strings")
        for item in self.users:
            if name == item.username:
                return item
        raise PythinuxError("Invalid user by name.")

    def remove(self, user):
        assertTrue(isinstance(user, User), "Can only remove User objects from the user list")
        if user.locked:
            raise PythinuxError("Cannot remove locked user")
        self.users.remove(user)

    def removeByName(self, name):
        did = False
        assertTrue(isinstance(name, str), "Usernames can only be strings")
        for item in self.users:
            if item.username == name:
                self.remove(item)
                did = True
        return did

    def list(self):
        return copy(self.users)

    def check(self, user):
        return user in self.list()

    def __len__(self):
        return len(self.users)

    def serialise(self):
        config = configparser.ConfigParser()
        for user in self.users:
            config[user.username] = user.serialise()
        return config

    def deserialise(self, config):
        for sect in config.sections():
            username = config.get(sect, "username")
            password = config.get(sect, "password")
            locked = config.getboolean(sect, "locked", fallback=False)
            disabled = config.getboolean(sect, "disabled", fallback=False)
            group = loadGroupList().byName(config.get(sect, "group", fallback="user"))
            user = User(group, username, password, disabled=disabled, locked=locked)
            self.users.append(user)


def copy(obj):
    """
    Tries copy.deepcopy(), then copy.copy(), then nothing to ensure nothing fails.
    To my knowledge, this is pointless.
    It's also potentially dangerous; it returns the same object without a copy if both copy.deepcopy() and copy.copy() fail.
    """
    try:
        return cp.deepcopy(obj)
    except Exception:
        try:
            return cp.copy(obj)
        except Exception:
            return obj


def verifyHash(plaintext, saltedHashString):
    """
    Verifies a hash.
    Args:
        plaintext: the string to check against.
        saltedHashString: a hash generated using hashString()
    Returns a boolean depending on whether or not the two match.
    """
    assertTrue(isinstance(plaintext, str), "Can only encode and decode strings")
    assertTrue(isinstance(saltedHashString, str), "Can only encode and decode strings")
    if KPARAM_ARTIFICIAL_DECRYPT_TIME:
        time.sleep(KPARAM_INT_ARTIFICIAL_DECRYPT_TIME)

    if KPARAM_DEBUGGING_VERIFYHASH:
        print("[debug] Called verifyHash()")

    salt = saltedHashString[-32:]
    hashed_plaintext = hashString(plaintext, salt)
    return hashed_plaintext == saltedHashString


def div(returnMode=False):
    """
    Prints 20 hyphen/dash symbols.
    """
    s = "--------------------"
    if returnMode:
        return s
    else:
        print(s)


def br():
    """
    Displays a "Press ENTER To continue" screen when called.
    """
    div()
    input("Press ENTER to continue.")


def parseInput(user, string, shell):
    """
    Function for parsing aliases. Internal only.
    """
    for item in aliases:
        if string == item:
            string = aliases[item]

    import re

    pattern = r"\$\((.*?)\)"
    matches = re.findall(pattern, string)
    for match in matches:
        o = giveOutput(match, user, shell=shell)
        match = "$({})".format(match)
        string = string.replace(match, o)

    return string


def main(user: User, prompt: str, sudoMode=False, shell="shell", doNotExecute=False):
    """
    Main function. Used to execute commands.
    Args:
        (User) user: the User object.
        (str) prompt: the command that gets exexuted.
        (bool) sudoMode: Passed to load_program().
        (str) shell: the name of the terminal that executes the command.
    """
    assertTrue(isinstance(user, User), "Can only call commands as a user")
    assertTrue(isinstance(prompt, str), "Commands must be strings")
    assertTrue(isinstance(sudoMode, bool), "sudoMode must be a boolean value")
    assertTrue(isinstance(shell, str), "Shell name must be a string")
    assertTrue(isinstance(doNotExecute, bool), "doNotExecute must be a boolean value")
    try:
        if prompt == "":
            return
        elif prompt == "logoff":
            return LOGOFFEVENT
        else:
            prompt = parseInput(user, prompt, shell)
            if doNotExecute:
                return prompt
            i = load_program(prompt, user, sudoMode, shell)
            os.chdir(evalDir(CURRDIR, user))
            if not i:
                print("ERROR: Bad command or file name.")
    except KeyboardInterrupt:
        return "Operation interrupted by user"


def saveAliases(aliases):
    """
    Saves an alias list.
    Args:
        aliases: a list grabbed from loadAliases().
    """
    assertTrue(isinstance(aliases, dict), "Aliases can only be a dict of strings")
    with open("config/alias.cfg", "wb") as f:
        pickle.dump(aliases, f)


def loadAliases():
    """
    Returns the list of aliases, or {} if there isn't one.
    """
    return aliases.copy()


def exposeObjects(module, objects):
    """
    Internal function that adds a dictionary containing objects to a module.
    The dictionary is in the format {name:object}.
    Returns the module with the objects exposed.
    """
    for object_name, obj in objects.items():
        setattr(module, object_name, obj)


def sudo(user, maxAttempts=10, incorrectAttempts=0):
    """
    Password authentication.
    Args:
        user: the user getting authenticated.
    Returns True if the user types their password,
    and False if they fail after 10 tries.
    """
    assertTrue(isinstance(user, User), "Not a User object")
    assertTrue(isinstance(maxAttempts, int), "Not an integer")
    assertTrue(isinstance(incorrectAttempts, int), "Not an integer")
    if incorrectAttempts >= maxAttempts:
        return False
    p = getpass(f"[sudo] password for {user.username}: ")
    if verifyHash(p, user.password):
        return True
    else:
        sudo(user, maxAttempts, incorrectAttempts + 1)


def splitString(string):
    """
    Used by main() for turning a string into a list of arguments.
    """
    # Find substrings enclosed in single quotes
    assertTrue(isinstance(string, str), "Not a string")
    pattern = r"'([^']*)'"
    matches = re.findall(pattern, string)

    # Replace single-quoted substrings with placeholders
    for i, match in enumerate(matches):
        placeholder = f"__{i}__"
        string = string.replace(f"'{match}'", placeholder)

    # Split the modified string based on spaces
    split_list = string.split()

    # Replace the placeholders with the original single-quoted substrings
    for i, item in enumerate(split_list):
        if item.startswith("__") and item.endswith("__"):
            index = int(item[2:-2])
            split_list[i] = matches[index]
    return split_list


def maxEscape():
    """
    Internal function.
    """
    z = {}
    for item in pdir:
        z[item] = eval(item)
    return z


def exposeAllVar(module):
    """
    This function is unused.
    Adds the contents of globals() to a module.
    """
    assertTrue(isinstance(module, type(__builtins__)), "Not a module")
    # Get the global namespace of the current program
    program_globals = globals()

    # Assign all variables to the module's namespace
    for var_name, var_value in program_globals.items():
        # Exclude built-in and special variables
        if not var_name.startswith("__"):
            setattr(module, var_name, var_value)


def addPythinuxModule(module, shared_objects, user):
    """
    Adds the Pythinux module to a module.
    Internal function only, please ignore.
    """
    assertTrue(isinstance(module, type(__builtins__)), "Not a module")
    assertTrue(isinstance(shared_objects, dict), "Not a dict")
    assertTrue(isinstance(user, User), "Not a user object")
    pythinux = createModule("pythinux")
    exposeObjects(pythinux, shared_objects)
    module.pythinux = pythinux
    return module


def openFile(filename, user, mode="r", **kwargs):
    """
    Custom open() operation.
    """
    assertTrue(isinstance(filename, str), "Not a string")
    assertTrue(isinstance(user, User), "Not a user")
    assertTrue(isinstance(mode, str), "Not a string")
    for file in BLOCKED_FILES:
        if file in filename:
            raise PythinuxError("Cannot open restricted file")
    if filename == "/dev/null":
        return io.StringIO()
    elif filename == "/dev/random":
        return DevRandomStringIO()
    elif filename == "/dev/urandom":
        return DevURandomStringIO()
    else:
        return open(evalDir(filename, user), mode, **kwargs)

def limitedOpenFile(filename, user, mode="r", **kwargs):
    if KPARAM_DEBUGGING_LIMITED_OPEN:
        print(filename)
    """
    A restricted variant of file.open() that resticts access to certain files and folders.
    """
    assertTrue(isinstance(filename, str), "Filename must be a string")
    assertTrue(isinstance(user, User), "User object must be specified for user")
    assertTrue(isinstance(mode, str), "Mode must be a string")
    def isDirValid(filename, user):
        for directory in [
            "/share",
            "/tmp",
            "/config",
            "~",
            "/home/{}".format(user.username),
        ]:
            if filename.startswith(directory):
                return True
        for file in USER_BLOCKED_FILES:
            if file in filename:
                return False

    if isDirValid(filename, user):
        return openFile(*args, **kwargs)
    else:
        raise PythinuxError(
            "Cannot open file in restricted directory: {}".format(filename)
        )

def listFiles(directory, user, **kwargs):
    if directory == "/":
        return sorted(os.listdir(file.evalDir("/", user), **kwargs) + ["dev"])
    elif directory == "/dev":
        return ["null", "random", "urandom"]
    else:
        return sorted(os.listdir(file.evalDir(directory, user), **kwargs))

def listDebuggers(user, include=True):
    file = evalDir("/config/debuggers", user)
    if os.path.isfile(file):
        with open(file) as f:
            return f.read().rstrip("\n").split("\n") + SYSTEM_DEBUGGERS if include else []
    else:
        return SYSTEM_DEBUGGERS if include else []


def confirmAction(message, default=True):
    """
    Confirmation dialogue. Requires a displayed message, and can choose the default.
    """
    print(message)
    response = "*"
    while response not in ["y", "n", ""]:
        response = input("[{}/{}] $".format("Y" if default else "y", "n" if default else "N")).lower()
    if response == "y":
        return True
    elif response == "n":
        return False
    else:
        return default

def addDebugger(debugger, user):
    if not debugger in list_loadable_programs(user):
        raise PythinuxError("Invalid program")
    if debugger in listDebuggers(user):
        ## It's already in there, no need to add it again
        return
    if not confirmAction("Are you sure you want to add '{}' to the list of debuggers? This will allow it to access API calls that can be used for debugging, which can also be used maliciously. Are you absolutely sure?".format(debugger), False):
        print("Action declined by user.", file=sys.stderr)
        return
    file = evalDir("/config/debuggers", user)
    with open(file, "a") as f:
        f.write("{}\n".format(debugger))

def removeDebugger(debugger, user):
    if not debugger in listDebuggers(user):
        return
    if debugger in SYSTEM_DEBUGGERS:
        raise PythinuxError("Cannot remove system debugger")
    if not confirmAction("Are you sure you want to remove '{}' from the list of debuggers? This may break certain programs."):
        print("Action declined by user.", file=sys.stderr)
        return
    file = evalDir("/config/debuggers", user)
    debuggers = [x for x in listDebuggers(user, False) if x != debugger]
    with open(file, "w") as f:
        f.write("\n".join(debuggers).rstrip("\n"))

def cleanupDebuggers(user):
    for debugger in listDebuggers(user):
        if debugger not in list_loadable_programs(user):
            removeDebugger(debugger, user)
    if listDebuggers(user, False) in [[], ['']]:
        file = evalDir("/config/debuggers", user)
        if os.path.isfile(file):
            os.remove(file)

def generateDebugAPI():
    debug = createModule("debug")
    debug.load_program = copy(debugLoadProgram)
    debug.list_debuggers = copy(listDebuggers)
    debug.grant_debugging = copy(addDebugger)
    debug.revoke_debugging = copy(removeDebugger)
    debug.cleanup = copy(cleanupDebuggers)
    debug.system = copy(SYSTEM_DEBUGGERS)
    return debug


def generateAPI(module, user, sudoMode):
    """
    Exposes Pythinux 3.x API calls to a module.
    """
    
    assertTrue(isinstance(module, type(__builtins__)), "Not a module")
    assertTrue(isinstance(user, User), "Not a user")
    assertTrue(isinstance(sudoMode, bool), "Not a boolean")


    def isUnix():
        return unixMode

    ## Define API modules
    shell = createModule("shell")
    file = createModule("file")

    ## Add functions to modules
    shell.isUnix = copy(isUnix)
    file.evalDir = copy(evalDir)
    file.root = lambda: changeDirectory("/", user)
    file.changeDirectory = copy(changeDirectory)
    file.listdir = copy(listFiles)

    if KPARAM_USE_LIMITED_OPEN:
        file.open = copy(limitedOpenFile) if not user.group.canSys else copy(openFile)
    else:
        file.open = copy(openFile)

    ## Attach to module
    module.shell = shell
    module.file = file



class CurrentGroup(Group):
    def __init__(self, group):
        assertTrue(isinstance(group, Group), "Not a group")
        self.name = copy(group.name)
        self.canApp = bool(group.canApp)
        self.canAppHigh = bool(group.canAppHigh)
        self.canSys = bool(group.canSys)
        self.canSudo = bool(group.canSudo)
        self.locked = bool(group.locked)


class CurrentUser(User):
    def __init__(self, user):
        assertTrue(isinstance(user, User), "Not a user")
        self.username = copy(user.username)
        self.password = copy(user.password)
        self.group = CurrentGroup(user.group)


def isUserValid(user):
    assertTrue(isinstance(user, User), "Not a user")
    return user in userList


class ReadOnlyMeta(type):
    """
    Metaclass for ReadOnlyWrapper.
    """
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify unmodifiable object")

    def __delattr__(self, name):
        raise AttributeError("Cannot modify unmodifiable object")

class ReadOnlyWrapper(metaclass=ReadOnlyMeta):
    """
    A class that wraps around an object and makes it read-only by hijacking the __setattr__ method.
    Should be 100% API-compatible (however it doesn't work for standard types like strings and bools).
    """
    def __init__(self, obj):
        object.__setattr__(self, '_ReadOnlyWrapper__wrapped_obj', obj)

    def __getattr__(self, name):
        return getattr(self.__wrapped_obj, name)

    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify unmodifiable value")

    def __delattr__(self, name):
        raise AttributeError("Cannot modify unmodifiable value")

    def __dir__(self):
        return [name for name in dir(self.__wrapped_obj) if not name.startswith('_')]

    def __repr__(self):
        return f"ReadOnlyWrapper({repr(self.__wrapped_obj)})"

    def __str__(self):
        return str(self.__wrapped_obj)


def deprecatedOpen(*args, **kwargs):
    warnings.warn("open() is deprecated and will be removed in Pythinux 3.3, use file.open() instead", DeprecationWarning)
    return open(*args, **kwargs)

def loadProgramBase(
    program_name_with_args,
    user,
    sudoMode=False,
    shell="terminal",
    __name__=None,
    isolatedMode=False,
    libMode=False,
):
    def getTerm():
        return shell

    if not verifyUser(user) and KPARAM_ESCALATION_PROTECTION:
        raise PythinuxError("The User instance provided is corrupt. Refusing to execute.")
    
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(sudoMode, bool), "Not a boolean")
    assertTrue(isinstance(isolatedMode, bool), "Not a boolean")
    assertTrue(isinstance(libMode, bool), "Not a boolean")
    assertTrue(isinstance(shell, str), "Not a string")

    if KPARAM_DEBUGGING_LOAD_PROGRAM:
        print("load_program(prog='{}', user='{}', sudoMode={}, shell='{}', isolatedMode={}, libMode={})".format(
            program_name_with_args, user.username, sudoMode, sudoMode, shell, isolatedMode, libMode))

    current_directory = evalDir("/", user)
    system_directory = evalDir("/system", user)
    lsystem_directory = evalDir("/system_low", user)
    app_directory = evalDir("/app", user)
    happ_directory = evalDir("/app_high", user)
    lib_directory = evalDir("/lib", user)
    hlib_directory = evalDir("/lib_high", user)
    syslib_directory = evalDir("/system_lib", user)

    directories = [lsystem_directory, app_directory]
    if user.group.canAppHigh or sudoMode:
        directories.append(system_directory)
        directories.append(happ_directory)

    if libMode:
        directories.append(lib_directory)
        directories.append(syslib_directory)
        if user.group.canAppHigh or sudoMode:
            directories.append(hlib_directory)

    for directory in directories:
        program_parts = splitString(program_name_with_args)

        if len(program_parts) > 0:
            program_name = program_parts[0]
            args = program_parts[1:]
        else:
            program_name = ""
            args = []
        if program_name not in list_loadable_programs(user, sudoMode, libMode):
            return
        program_path = os.path.join(directory, program_name + ".py")
        script_path = os.path.join(directory, program_name + ".xx")
        if os.path.exists(script_path):
            with open(script_path) as f:
                run_script(f, user)
            return
        if os.path.exists(program_path):
            if not __name__:
                __name__ = program_name
            module_spec = importlib.util.spec_from_file_location(
                program_name, program_path
            )
            module = importlib.util.module_from_spec(module_spec)
            sp = copy(sys.path)
            sp.insert(0, "app")

            shared_objects = {
                "Base": copy(Base),
                "__name__": copy(__name__),
                "currentUser": CurrentUser(user),
                "div": copy(div),
                "br": copy(br),
                "load_program": copy(load_program) if program_name in listDebuggers(user) else copy(limitedLoadProgram),
                "list_loadable_programs": copy(list_loadable_programs),
                "version": copy(version),
                "hashString": copy(hashString),
                "verifyHash": copy(verifyHash),
                "pprint_dict": copy(pprint_dict),
                "pprint": copy(pprint),
                "obj_to_dict": copy(obj_to_dict),
                "os": copy(os),
                "alias": copy(aliases),
                "cls": copy(cls),
                "doCalc": copy(doCalc),
                "mergeDict": copy(mergeDict),
                "copy": copy(copy),
                "getTerm": copy(getTerm),
                "currentProgram": copy(program_name),
                "osName": copy(osName),
                "FileError": copy(FileError),
                "createModule": copy(createModule),
                "silent": copy(silent),
                "giveVars": copy(giveVars),
                "attachDebugger": copy(attachDebugger),
                "PythinuxError": copy(PythinuxError),
                "CURRDIR": copy(CURRDIR),
                "ROOTDIR": copy(ROOTDIR),
                "verifyUser": copy(verifyUser),
                "CurrentUser": copy(CurrentUser),
                "isRoot": FalseValue(),
                "assertTrue": copy(assertTrue),
                "isDebugger": FalseValue(),
                "ReadOnlyWrapper": copy(ReadOnlyWrapper),
            }
            
            if directory in [
                system_directory,
                lsystem_directory,
                happ_directory,
                syslib_directory,
            ]:
                sp.insert(0, "app_high")
                system_objects = {
                    "User": copy(User),
                    "Group": copy(Group),
                    "GroupList": copy(GroupList),
                    "UserList": copy(UserList),
                    "loadGroupList": copy(loadGroupList),
                    "saveGroupList": copy(saveGroupList),
                    "loadUserList": copy(loadUserList),
                    "saveUserList": copy(saveUserList),
                    "currentUser": user,
                    "aliases": aliases,
                    "userList": userList,
                    "groupList": groupList,
                    "saveAliases": copy(saveAliases),
                    "createUser": copy(createUser),
                    "saveUserList": saveUserList,
                    "runCommand": copy(main),
                    "saveAL": copy(saveAL),
                    "clearTemp": copy(clearTemp),
                    "run_script": copy(run_script),
                    "removeUser": copy(removeUser),
                    "loginScreen": copy(loginScreen),
                    "LOGOFFEVENT": copy(LOGOFFEVENT),
                    "parseInput": copy(parseInput),
                    "isRoot": TrueValue(),
                }

                shared_objects.update(system_objects)

            if KPARAM_DEPRECATE_OPEN:
                shared_objects.update({"open": deprecatedOpen})

            # Expose the objects to the loaded program
            if isolatedMode:
                shared_objects = {}
            exposeObjects(module, shared_objects)
            generateAPI(module, user, sudoMode)
            # Add custom sys.path
            d = {
                "sys": copy(sys),
                "sys.path": copy(sp),
            }
            exposeObjects(module, d)
            # Set arguments as a custom attribute
            module.arguments = args
            module.args = args

            if program_name in listDebuggers(user):
                module.debug = generateDebugAPI()
                module.isDebugger = TrueValue()

            # Add Pythinux module
            module = addPythinuxModule(module, shared_objects, user)
            return module, module_spec


def isProgramReal(program_name, user, sudoMode, libMode):
    assertTrue(isinstance(program_name, str), "Not a string")
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(sudoMode, bool), "Not a boolean")
    assertTrue(isinstance(libMode, bool), "Not a boolean")

    return program_name in list_loadable_programs(user, sudoMode, libMode)


def changeDirectory(directory: str, user: User):
    assertTrue(isinstance(directory, str), "Not a string")
    assertTrue(isinstance(user, User), "Not a user object")
    if not KPARAM_REAL_DIRECTORY:
        return
    CURRDIR = directory
    os.chdir(evalDir(directory, user))


def evalDir(directory: str, user: User):
    """
    Evaluates a directory, turning a path like "/home/root" to a full directory.
    Supports:
        `.` - Resolves to current directory.
        `..` - Resolves to previous directory.
        `~` - User's home directory.
        `/` - Evaluates to root directory.

    Also ensures no directory above the root directory is selected, ensuring no
    VM escapes occur.
    """
    assertTrue(isinstance(directory, str), "Not a string")
    assertTrue(isinstance(user, User), "Not a user object")
    if directory in EVALHIST:
        return directory
    directory = directory.replace("\\", "/")
    if directory.startswith(".") and not directory.endswith(".."):
        directory = directory.replace(".", CURRDIR, 1)
    elif directory.startswith("~"):
        directory = directory.replace("~", "/home/{}".format(user.username), 1)
    else:
        directory = "{}{}".format(CURRDIR, directory)

    if directory.startswith("/"):
        directory = directory.replace("/", ROOTDIR + "/", 1)

    if directory.endswith(".."):
        parts = directory.split("/")
        parts.pop()
        parts.pop()
        directory = "/".join(parts)

    if not directory.startswith(ROOTDIR):
        return ROOTDIR
    else:
        directory = directory.replace("//", "/")
        EVALHIST.append(directory)
        return directory


def load_program(
    program_name_with_args,
    user,
    sudoMode=False,
    shell="terminal",
    __name__=None,
    isolatedMode=False,
    libMode=False,
):
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(sudoMode, bool), "Not a boolean")
    assertTrue(isinstance(isolatedMode, bool), "Not a boolean")
    assertTrue(isinstance(libMode, bool), "Not a boolean")
    assertTrue(isinstance(shell, str), "Not a string")

    if program_name_with_args == "":
        return

    program_name = program_name_with_args.split(" ")[0]
    if not isProgramReal(program_name, user, sudoMode, libMode):
        return

    module, module_spec = loadProgramBase(
        program_name_with_args,
        user,
        sudoMode,
        shell,
        __name__,
        isolatedMode,
        libMode,
    )
    if module:
        module_spec.loader.exec_module(module)
        if not libMode:
            if not "main" in dir(module):
                print("warning: {} has no main(), in future this will throw a PythinuxError".format(program_name))
            else:
                module.main(module.args)
        return ReadOnlyWrapper(module) if KPARAM_USE_MODULE_WRAPPER else module


def limitedLoadProgram(program, user, **kwargs):
    """
    A variant of load_program() that cannot load debuggers. Used for security purposes.
    """
    if not program:
        return
    args = program.split(" ")
    if args[0] in listDebuggers(user):
        return 
    else:
        return load_program(program, user, **kwargs)

def debugLoadProgram(*args, **kwargs):
    useWrapper = bool(KPARAM_USE_MODULE_WRAPPER)
    KPARAM_USE_MODULE_WRAPPER = False
    prog = load_program(*args, **kwargs)
    KPARAM_USE_MODULE_WRAPPER = bool(useWrapper)
    return prog



def clearTemp(user):
    """
    Clears the contents of the tmp/ directory in the
    Pythinux install directory.
    """
    assertTrue(isinstance(user, User), "Not a user object")
    try:
        shutil.rmtree(evalDir("/tmp", user))
    except Exception:
        pass
    try:
        os.mkdir(evalDir("/tmp", user))
    except Exception:
        pass


def saveAL(username):
    """
    Makes username the autologin username
    Autologin allows for only the password to be entered.
    """
    assertTrue(isinstance(username, str), "Usernames must be strings")
    with open("config/autologin.cfg", "w") as f:
        f.write(username)


def loadAL():
    """
    Returns the autologin username as a string, or None of there isn't one set.
    """
    try:
        with open("config/autologin.cfg") as f:
            return f.read()
    except Exception:
        return


def cls():
    """
    Clears the terminal screen.
    Works for both Windows and Unix-like systems, so basically everything.
    """
    if KPARAM_DISABLE_CLS:
        return
    res = platform.uname()
    os.system("cls" if res[0] == "Windows" else "clear")


def run_script(f, user):
    """
    Runs a script.
    Args:
        f: a file-type object to be read. Must be in 'r' mode.
        user: a User object, the actual user to execute the script.
    """
    warnings.warn("run_script() will be removed in Pythinux 3.2 - use shell.run_script() instead", DeprecationWarning)
    for item in f.read().split("\n"):
        main(user, item, shell="script")


def list_loadable_programs(user, sudoMode=False, libMode=False):
    """
    Returns a list of all commands that the user is authorised to load.
    Note: if sudoMode is True, the app and system
    directories are always authorised.
    """
    assertTrue(isinstance(user, User), "Not a user object")
    assertTrue(isinstance(sudoMode, bool), "Not a boolean")
    assertTrue(isinstance(libMode, bool), "Not a boolean")

    current_directory = evalDir("/", user)
    system_directory = evalDir("/system", user)
    lsystem_directory = evalDir("/system_low", user)
    app_directory = evalDir("/app", user)
    happ_directory = evalDir("/app_high", user)
    lib_directory = evalDir("/lib", user)
    hlib_directory = evalDir("/lib_high", user)
    syslib_directory = evalDir("/system_lib", user)

    directories = [lsystem_directory]
    if user.group.canApp:
        directories.append(app_directory)
    if user.group.canSys:
        directories.append(system_directory)
    if user.group.canAppHigh:
        directories.append(happ_directory)
    loadable_programs = set()
    if libMode:
        directories.append(lib_directory)
        directories.append(syslib_directory)
        if sudoMode or user.group.canSys:
            directories.append(hlib_directory)

    for directory in directories:
        if os.path.exists(directory) and os.path.isdir(directory):
            programs = [f[:-3] for f in os.listdir(directory) if f.endswith(".py")]
            loadable_programs.update(programs)

    if os.path.exists(app_directory) and os.path.isdir(app_directory):
        programs = [
            "*" + f[:-3] for f in os.listdir(app_directory) if f.endswith(".xx")
        ]
        loadable_programs.update(programs)

    return sorted(loadable_programs)


def init(user):
    """
    Init function.
    """
    assertTrue(isinstance(user, User), "Not a user object")
    main(user, "cls")
    shell = load_program("shell", user, libMode=True)
    shell.init(user)
    shell.terminal(user)


def saveUserList(userList):
    """
    Saves a userlist to the file system.
    userlist: a userlist (returned by loadUserList()).
    """
    assertTrue(isinstance(userList, UserList), "Not a UserList object")
    if isinstance(userList, UserList):
        config = userList.serialise()
        with open(
            evalDir("/config/users.ini", User(Group("tempgroup"), "tempuser", "")), "w"
        ) as f:
            config.write(f)
    else:
        raise PythinuxError("Cannot save invalid userlist.")


def loadUserList():
    """
    Handles loading the userlist from the file system.
    Returns the userlist when called.
    """
    try:
        userList = UserList()
        config = configparser.ConfigParser()
        config.read(evalDir("/config/users.ini", User(Group("tempgroup"), "tempuser")))
        userList.deserialise(config)
        return userList
    except Exception:
        return UserList()


def loginScreen(username=None, password=None):
    """
    Login screen.
    Args:
        (optional) (str) username: the username passed to the login screen.
        Passing this will launch the Unlock Screen screen.
        (optional) (str) password: the password passed to the login screen.
        Passing both the username and password bypasses the input.
    Once you enter your details, init() is called.
    """
    cls()
    if not password:
        div()
        print("Unlock System" if username else "Pythinux Login Screen")
        div()
        x = True
    else:
        x = False
    if not username:
        username = input("Username $")
    if not password:
        password = getpass("Password $")
    for item in loadUserList().users:
        if item.check(username, password) and not item.disabled:
            init(item)
            return
    cls()
    div()
    print("Incorrect username/password sequence.")
    br()
    loginScreen()


def makeDir():
    """
    Don't remember what this one does. Internal function. Ignore.
    """
    z = []
    for i in pdir:
        z.append(eval(i))
    return z


def makeDirDict():
    """
    Returns a dictionary containing
    every single item in dir() in the format {itemname:item}.
    Mostly unused.
    """
    m = makeDir()
    index = 0
    z = {}
    for item in pdir:
        z[item] = m[index]
        index += 1
    return z


def removeUser(userlist, user):
    """
    Removes a user from the userlist.
    Args:
        userlist: a userlist object (loaded from loadUserList())
        user: a User instance.
    Returns:
        userlist: a userlist that can be passed to saveUserList().
    """
    assertTrue(isinstance(userList, UserList), "Not a UserList object")
    assertTrue(isinstance(user, User), "Not a User object")

    try:
        shutil.rmtree(f"home/{user.username}")
    except Exception:
        pass
    userlist.remove(user)
    saveUserList(userlist)


def createUser(userlist, user):
    """
    Adds a User to a userlist.
    Args:
        userlist: a userlist object (loaded from loadUserList())
        user: a User instance.
    Returns:
        userlist: a userlist that can be passed to saveUserList().
    """
    assertTrue(isinstance(userList, UserList), "Not a UserList object")
    assertTrue(isinstance(user, User), "Not a User object")

    if not isinstance(userlist, UserList) or not isinstance(user, User):
        raise TypeError
    for item in userlist.list():
        if item.username == user.username:
            removeUser(userlist, item)
    for directory in ["~", "~/config", "~/doc", "~/download"]:
        try:
            os.mkdir(evalDir(directory, user))
        except FileExistsError:
            pass
    with open(evalDir("~/shellrc.xx", user), "w") as f:
        f.write(DEFAULT_SHELL_SCRIPT)
    userlist.add(user)
    return userlist


def mergeDict(a, b):
    """
    Merges a with b.
    Args:
        a: dictionary. Main dictionary.
        b: dictionary.
    Returns:
        a with the contents of b appended to it.
    """
    assertTrue(isinstance(a, dict), "Not a dictionary")
    assertTrue(isinstance(b, dict), "Not a dictionary")

    result = a.copy()

    for key, value in b.items():
        if key not in a:
            result[key] = value

    return result


def obj_to_dict(obj, addItemType=True):
    """
    Recursively convert an object and all its attributes to a dictionary.
    """
    if isinstance(obj, (int, float, bool, str)):
        return obj
    if isinstance(obj, type):
        return f"<type '{obj.__name__}'>"
    if inspect.isclass(obj):
        return {"__class__": obj.__name__}

    if isinstance(obj, (tuple, list)):
        return [obj_to_dict(x) for x in obj]

    if isinstance(obj, dict):
        if addItemType:
            obj2 = {"@itemType": type({}).__name__}
        obj2.update(obj)
        obj = obj2
        return {key: obj_to_dict(value) for key, value in obj.items()}
    obj_dict = {}
    if addItemType:
        obj_dict["@itemType"] = type(obj).__name__
    for attr in dir(obj):
        if attr.startswith("__") and attr.endswith("__"):
            continue
        if attr == "dic":
            continue
        if getattr(obj, attr) is None:
            obj_dict[attr] = "<class 'none'>"
            continue
        if callable(getattr(obj, attr)):
            obj_dict[attr] = f"<function '{attr}'>"
            continue
        value = getattr(obj, attr)
        obj_dict[attr] = obj_to_dict(value)
    return obj_dict


def pprint_dict(dic):
    """
    Takes a dictionary and returns it as a string with indentation
    """
    import json
    return json.dumps(dic, indent=4)


def pprint(obj):
    """
    Prints an object's attributes as a formatted dictionary.
    """
    print(pprint_dict(obj_to_dict(obj)))


def setupWizard():
    """
    Setup wizard.
    * Sets up a user account, complete with username,
      password, init script, etc.
    * Sets up autologin, depending on user choice.
    """
    if os.path.isfile("../LICENSE"):
        cls()
        with open("../LICENSE") as f:
            div()
            print("Legal Licensing Information")
            div()
            print(f.read())
            br()
    cls()
    print(f"{div(True)}\nSetup Wizard\n{div(True)}")
    username = ""
    while not username:
        username = input("Enter Your Username $")
        if username == "":
            print("ERROR: You must enter a username.")
        if username in ["root"]:
            username = ""
            print("ERROR: That username is disallowed.")
    password = ""
    while password == "":
        password = getpass("Set A Password $")
        if password == "":
            print("Error: Cannot set blank password.")
    if password == "":
        password = None

    groupList = GroupList()
    g = groupList.byName("user")
    rootGroup = groupList.byName("root")
    user = User(rootGroup, username, hashString(password))
    root = User(rootGroup, "root", disabled=True, locked=True)
    userList = loadUserList()
    userList = createUser(userList, user)
    userList = createUser(userList, root)
    saveUserList(userList)

    if input("Set up autologin? [Y/n] $").lower() != "n":
        saveAL(username)
    cls()
    div()
    print("You have successfully set up Pythinux.")
    print("To get started, log in and run the `welcome` command.")
    br()


if __name__ == "__main__":
    try:
        os.chdir("pythinux")
        fixDirectories()
    except Exception:
        div()
        print("CRITICAL ERROR!")
        div()
        print("The Pythinux install directory has been removed.")
        print("This is normally a result of catastrophic user error.")
        print("Reinstall Pythinux from source:")
        print("https://codeberg.org/Pythinux/Pythinux")
        br()
    ROOTDIR = os.getcwd()
    CURRDIR = "/"
    global userList, groupList
    if loadUserList().users == []:
        setupWizard()
    userList = loadUserList()
    groupList = loadGroupList()
    global pdir
    aliases = loadAliases()
    pdir = dir()
    loginScreen(loadAL())

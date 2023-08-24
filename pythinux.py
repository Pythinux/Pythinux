#!/usr/bin/python
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
from io import StringIO
from getpass import getpass

global osName, version, cdir, var
osName = "Pythinux"
version = [2, 5, 0]
var = {}


class PythinuxError(Exception):
    """
    Exception thrown by the kernel when an issue occurs.
    """

    def __init__(self, text):
        self.text = str(text)

    def __str__(self):
        return self.text


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
    l = [
        "app",
        "app_high",
        "config",
        "home",
        "lib",
        "log",
        "rscript",
        "tmp",
    ]
    if returnMode:
        return l
    for item in l:
        if not os.path.isdir(item):
            os.mkdir(item)


def castObject(obj, new_type):
    """
    Create a new object of a specified type or use an existing object,
    copying all attributes (excluding methods) of the
    original object to the new one.

    Args:
        obj: The original object to cast
        cast_type: The type or object to cast the original object to.
        If `cast_type` is a type, a new object of that type is created.
        If `cast_type` is an object, the original object is
        copied to that object.

    Returns:
        A new object of the specified type, with all attributes
        (excluding methods) of the original object copied over.
        If `cast_type` is an object, the original object is copied to
        that object and returned.
    """
    if isinstance(new_type, type):
        new_obj = new_type()
    else:
        new_obj = new_type

    for key, value in obj.__dict__.items():
        if not callable(value):
            setattr(new_obj, key, value)

    return new_obj


def setVars(var):
    """
    Unused.
    """
    var = var


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
    Runs some code without outputting anything to the terminal
    Args:
    function: a callable object.
    """
    stdout = sys.stdout
    sys.stdout = None
    x = function()
    sys.stdout = stdout
    return x


def CompileOS():
    print("Clear begin.")
    """
    Clears your installation of Pythinux.
    """
    # clear directories
    for item in fixDirectories(True):
        if os.path.isdir(item):
            shutil.rmtree(item)
            os.mkdir(item)

    for path, dirs, files in os.walk(os.getcwd()):
        for item in dirs:
            try:
                shutil.rmtree("__pycache__")
            except Exception:
                pass
    print("Cleared Pythinux install.")


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


def createService(command, user):
    """
    Creates a service that can be passed to startService().
    Args:
        command: command to be executed.
        user: user that executes the command.
    """
    return threading.Thread(target=main, args=(command, user))


def startService(thread, name):
    """
    Starts a service.
    Args:
    thread: a service generated using createService()
    name: name of the service.
    """
    thread.name = name
    thread.start()


def attachDebugger(globals):
    import code

    code.InteractiveConsole(locals=globals)


def giveOutput(command, user, split=False, shell="terminal"):
    """
    Returns the output of a command.
    Positional arguments:
        (str) command: the command to execute
        (User) user: the user executing the command. Pass currentUser.
        (bool) split: if true, returns it split into a list with \n as a
        separator.
        (str) shell: Passed to main().
    """
    # Redirect stdout to a buffer
    stdout_backup = sys.stdout
    sys.stdout = StringIO()

    # Call the function
    main(user, command, shell=shell)

    # Get the output from the buffer
    output = sys.stdout.getvalue()

    # Restore stdout
    sys.stdout = stdout_backup
    if split:
        return output.split("\n")
    else:
        return output


def doCalc(text):
    """
    A fully safe (but very restricted) version of eval().
    Undergoes HEAVY sanitisation before execution.
    """
    allowed_nodes = (ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Num)
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


class SudoError(Exception):
    """
    Generic exception for issues with sudo priveleges.
    """

    def __str__(self):
        return "Insufficient priveleges to execute action."


class LOGOFFEVENT:
    """
    This class(not an instance of it) is returned by main() when
    the user uses the "logoff" command.
    """


def hashString(plaintext, salt=None):
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
    Used to prevent linter programs from complaining about "unused" programs.
    """
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
        canSysHigh=False,
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
        canSysHigh: Boolean. Defines whether or not the user can access system
            apps in the "system_high" directory.
        canSudo: Boolean. Determines whether or not the user can use `sudo`.
        """
        self.name = name.lower()
        self.canApp = canApp
        self.canAppHigh = canAppHigh
        self.canSys = canSys
        self.canSysHigh = canSysHigh
        self.canSudo = canSudo
        self.locked = locked


class GroupList(Base):
    """
    GroupList class for use in saveGroupList()/loadGroupList().
    """

    def __init__(self):
        self.groups = [
            Group("guest"),
            Group("user", True, canSudo=True, locked=True),
            Group("root", True, True, True, canSudo=True, locked=True),
            Group("god", True, True, True, True, True),
        ]

    def add(self, group):
        """
        Adds a group to the GroupList.
        Args:
        * group: a Group instance.
        """
        if isinstance(group, Group):
            self.groups.append(group)
        else:
            raise PythinuxError("Cannot add a non-Group object a GroupList.")

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
        for item in self.groups:
            if item.name == name:
                return item

    def __len__(self):
        return len(self.groups)


class CurrentProgram:
    def __init__(self, name):
        self._name = name
        self._modifiable = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._modifiable:
            self._name = value
        else:
            raise AttributeError(
                "Cannot modify name after object construction"
            )

    def __class__(self):
        return type

    def lock_class(self):
        self._modifiable = False


class User(Base):
    """
    User class used by Pythinux.
    See __init__() for how to create User objects properly.
    """

    def __init__(self, group, username, password=hashString(""), hidden=False):
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
        self.group = group
        self.username = username
        self.password = hashString(password)
        self.hidden = hidden

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
        """
        Returns whether or not the user's level is 2 or higher,
        indicating a root user.
        """
        return self.group.canAppHigh

    def god(self):
        """
        Returns whether or not the user's level is 3 or higher,
        indicating a god user.
        """
        return self.group.canSysHigh

    def USERTYPE(self):
        """
        Returns the name of the user's group.
        """
        return self.group.name


class UserList(Base):
    def __init__(self):
        self.users = []
        self.append = self.add

    def add(self, user):
        """
        Adds a user to the user list.
        """
        if isinstance(user, User):
            self.users.append(user)
        else:
            raise PythinuxError("Invalid User to add to userlist.")

    def byName(self, name):
        """
        Returns the first instance of
        a user in the userlist with the same name.
        """
        for item in self.users:
            if name == item.username:
                return item
        raise PythinuxError("Invalid user by name.")

    def remove(self, user):
        self.users.remove(user)

    def removeByName(self, name):
        did = False
        for item in self.users:
            if item.username == name:
                self.users.remove(item)
                did = True
        return did

    def list(self):
        return copy(self.users)

    def __len__(self):
        return len(self.users)


def copy(obj):
    """
    See python's copy.deepcopy(). It's the same thing.
    """
    try:
        return cp.deepcopy(obj)
    except Exception:
        try:
            return cp.copy(obj)
        except Exception:
            return obj


def logEvent(text, log="base_log"):
    """
    Creates or appends to a log.
    Arguments:
        (str) text: the text that gets logged.
        (str) log: the name of the log file. Default is "base_log".
    """
    try:
        with open(f"log/{log}.log", "a") as f:
            f.write(text + "\n")
    except Exception:
        with open(f"log/{log}.log", "w") as f:
            f.write(text + "\n")


def verifyHash(plaintext, saltedHashString):
    """
    Verifies a hash.
    Args:
        plaintext: the string to check against.
        saltedHashString: a hash generated using hashString()
    Returns a boolean depending on whether or not the two match.
    """
    salt = saltedHashString[-32:]
    hashed_plaintext = hashString(plaintext, salt)
    return hashed_plaintext == saltedHashString

    return hashed_plaintext == saltedHashString


def sha256(string, salt=None):
    """
    Performs a SHA256 og a string.
    Arguments:
        (str) string: string to be parsed
        (bytes-like) salt: optional salt, should be output of os.urandom().
    """
    if string:
        return hashString(string, salt)
    else:
        return


class rangedInt:
    """
    A floating point number with a specified range
    that gets automatically adhered to.
    Currently unused, but will be used soon.
    """

    def __init__(self, value, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self._value = None
        self.set(value)

    def get(self):
        return self._value

    def set(self, value):
        if value < self.min_value:
            self._value = self.min_value
        elif value > self.max_value:
            self._value = self.max_value
        else:
            self._value = int(value)

    def __str__(self):
        return str(self._value)

    def __add__(self, other):
        if isinstance(other, rangedInt):
            return rangedInt(
                self._value + other.get(), self.min_value, self.max_value
            )
        elif isinstance(other, (int, float)):
            return rangedInt(
                self._value + other, self.min_value, self.max_value
            )
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, rangedInt):
            return rangedInt(
                self._value - other.get(), self.min_value, self.max_value
            )
        elif isinstance(other, (int, float)):
            return rangedInt(
                self._value - other, self.min_value, self.max_value
            )
        else:
            return NotImplemented

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, rangedInt):
            return rangedInt(
                self._value * other.get(), self.min_value, self.max_value
            )
        elif isinstance(other, (int, float)):
            return rangedInt(
                self._value * other, self.min_value, self.max_value
            )
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, rangedInt):
            return rangedInt(
                self._value / other.get(), self.min_value, self.max_value
            )
        elif isinstance(other, (int, float)):
            return rangedInt(
                self._value / other, self.min_value, self.max_value
            )
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        return self.__truediv__(other)


def div():
    """
    Prints 20 hyphen/dash symbols.
    """
    print("--------------------")


def div2():
    """
    Returns 20 hyphen/dash symbols as a string.
    """
    return "--------------------"


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


def main(user, prompt, sudoMode=False, shell="terminal", doNotExecute=False):
    """
    Main function. Used to execute commands.
    Args:
        (User) user: the User object.
        (str) prompt: the command that gets exexuted.
        (bool) sudoMode: Passed to load_program().
        (str) shell: the name of the terminal that executes the command.
    """
    try:
        global cdir
        if prompt == "":
            return
        elif prompt == "logoff":
            return LOGOFFEVENT
        else:
            prompt = parseInput(user, prompt, shell)
            if doNotExecute:
                return prompt
            i = load_program(prompt, user, sudoMode, shell)
            os.chdir(cdir)
            if not i:
                print("Bad command or file name:", prompt)
    except Exception as e:
        e = doNothing(e)
        return traceback.format_exc()
    except KeyboardInterrupt:
        return "Operation interrupted by user"


def saveAliases(aliases):
    """
    Saves an alias list.
    Args:
        aliases: a list grabbed from loadAliases().
    """
    with open("config/alias.cfg", "wb") as f:
        pickle.dump(aliases, f)


def loadAliases():
    """
    Returns the list of aliases, or {} if there isn't one.
    """
    try:
        with open("config/alias.cfg", "rb") as f:
            return pickle.load(f)
    except Exception:
        saveAliases({})
        return {}


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
    pythinux = createModule("pythinux")
    exposeObjects(pythinux, shared_objects)
    module.pythinux = pythinux
    return module


def loadProgramBase(
    program_name_with_args,
    user,
    sudoMode=False,
    shell="terminal",
    __name__=None,
    isolatedMode=False,
):
    def getTerm():
        return shell

    if user.god():
        sudoMode = True
    current_directory = os.getcwd()
    system_directory = os.path.join(current_directory, "system")
    hsystem_directory = os.path.join(current_directory, "system_high")
    lsystem_directory = os.path.join(current_directory, "system_low")
    app_directory = os.path.join(current_directory, "app")
    happ_directory = os.path.join(current_directory, "app_high")

    directories = [system_directory, lsystem_directory, app_directory]
    if user.admin() or sudoMode:
        directories.append(system_directory)
        directories.append(happ_directory)
    if user.god():
        directories.append(hsystem_directory)
    for directory in directories:
        program_parts = splitString(program_name_with_args)

        if len(program_parts) > 0:
            program_name = program_parts[0]
            args = program_parts[1:]
        else:
            program_name = ""
            args = []
        if program_name not in list_loadable_programs(user, sudoMode):
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
                "castObject": copy(castObject),
                "Base": copy(Base),
                "__name__": copy(__name__),
                "currentUser": copy(user),
                "div": copy(div),
                "div2": copy(div2),
                "br": copy(br),
                "load_program": copy(load_program),
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
                "logEvent": copy(logEvent),
                "getTerm": copy(getTerm),
                "currentProgram": copy(program_name),
                "giveOutput": copy(giveOutput),
                "osName": copy(osName),
                "FileError": copy(FileError),
                "startService": copy(startService),
                "createModule": copy(createModule),
                "silent": copy(silent),
                "setVars": copy(setVars),
                "giveVars": copy(giveVars),
                "createService": copy(createService),
                "attachDebugger": copy(attachDebugger),
            }
            if directory in [
                system_directory,
                hsystem_directory,
                lsystem_directory,
                happ_directory,
            ]:
                sp.insert(0, "app_high")
                system_objects = {
                    "cdir": copy(cdir),
                    "User": copy(User),
                    "Group": copy(Group),
                    "GroupList": copy(GroupList),
                    "UserList": copy(UserList),
                    "loadGroupList": copy(loadGroupList),
                    "saveGroupList": copy(saveGroupList),
                    "currentUser": user,
                    "aliases": aliases,
                    "userList": userList,
                    "groupList": groupList,
                    "saveAliases": copy(saveAliases),
                    "createUser": copy(createUser),
                    "saveUserList": saveUserList,
                    "main": copy(main),
                    "saveAL": copy(saveAL),
                    "clearTemp": copy(clearTemp),
                    "run_script": copy(run_script),
                    "removeUser": copy(removeUser),
                    "sudo": copy(sudo),
                    "loginScreen": copy(loginScreen),
                    "LOGOFFEVENT": copy(LOGOFFEVENT),
                    "load_program": copy(load_program),
                    "parseInput": copy(parseInput),
                }
                if user.god():
                    system_objects["CompileOS"] = copy(CompileOS)
                    system_objects["setupWizard"] = copy(setupWizard)
                shared_objects.update(system_objects)
            # Expose the objects to the loaded program
            if isolatedMode:
                shared_objects = {}
            exposeObjects(module, shared_objects)
            # Add custom sys.path
            d = {
                "sys": copy(sys),
                "sys.path": copy(sp),
            }
            exposeObjects(module, d)
            # Set arguments as a custom attribute
            module.arguments = args
            module.args = args

            # Add Pythinux module
            module = addPythinuxModule(module, shared_objects, user)
            return module, module_spec


def load_program(
    program_name_with_args,
    user,
    sudoMode=False,
    shell="terminal",
    debugMode=False,
    baseMode=False,
    __name__=None,
    isolatedMode=False,
):
    if debugMode:
        print(
            "### Load Arguments:",
            [program_name_with_args, user, sudoMode, shell, __name__],
        )
    try:
        module, module_spec = loadProgramBase(
            program_name_with_args,
            user,
            sudoMode,
            shell,
            __name__,
            isolatedMode,
        )
        if baseMode:
            return module, module_spec
    except Exception:
        return
    if module:
        if debugMode:
            print("### Arguments:", module.args)
        module_spec.loader.exec_module(module)
        return module


def clearTemp():
    """
    Clears the contents of the tmp/ directory in the
    Pythinux install directory.
    """
    try:
        shutil.rmtree("tmp")
    except Exception:
        pass
    try:
        os.mkdir("tmp")
    except Exception:
        pass


def saveAL(username):
    """
    Makes username the autologin username
    Autologin allows for only the password to be entered.
    """
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
    res = platform.uname()
    os.system("cls" if res[0] == "Windows" else "clear")


def run_script(f, user):
    """
    Runs a script.
    Args:
        f: a file-type object to be read. Must be in 'r' mode.
        user: a User object, the actual user to execute the script.
    """
    for item in f.read().split("\n"):
        main(user, item, shell="script")


def list_loadable_programs(user, sudoMode=False):
    """
    Returns a list of all commands that the user is authorised to load.
    Note: if sudoMode is True, the app and system
    directories are always authorised.
    """
    current_directory = os.getcwd()
    system_directory = os.path.join(current_directory, "system")
    app_directory = os.path.join(current_directory, "app")
    current_directory = os.getcwd()
    system_directory = os.path.join(current_directory, "system")
    hsystem_directory = os.path.join(current_directory, "system_high")
    lsystem_directory = os.path.join(current_directory, "system_low")
    app_directory = os.path.join(current_directory, "app")
    happ_directory = os.path.join(current_directory, "app_high")

    directories = [lsystem_directory]
    if user.group.canApp:
        directories.append(app_directory)
    if user.group.canSys:
        directories.append(system_directory)
    if user.group.canAppHigh:
        directories.append(happ_directory)
    if user.group.canSysHigh:
        directories.append(hsystem_directory)
    loadable_programs = set()

    for directory in directories:
        if os.path.exists(directory) and os.path.isdir(directory):
            programs = [
                f[:-3] for f in os.listdir(directory) if f.endswith(".py")
            ]
            loadable_programs.update(programs)

    if os.path.exists(app_directory) and os.path.isdir(app_directory):
        programs = [
            "*" + f[:-3]
            for f in os.listdir(app_directory)
            if f.endswith(".xx")
        ]
        loadable_programs.update(programs)

    return sorted(loadable_programs)


def init(user, x):
    """
    Init function. Runs the  'initd --init' command.
    """
    main(user, "cls")
    if user.god() and x:
        div()
        print("God Warning")
        div()
        print("You have logged in as a God account.")
        print("Do not use a God account unless you HAVE to.")
        print(
            "If you are unaware of the security risks of using"
            + ' a God account, type "logoff".'
        )
        div()
    main(user, "initd --init")
    sys.exit()


def saveUserList(userList):
    """
    Saves a userlist to the file system.
    userlist: a userlist (returned by loadUserlist()).
    """
    if isinstance(userList, UserList):
        with open("config/users.cfg", "wb") as f:
            pickle.dump(userList, f)
    else:
        raise PythinuxError("Cannot save invalid userlist.")


def loadUserList():
    """
    Handles loading the userlist from the file system.
    Returns the userlist when called.
    """
    try:
        with open("config/users.cfg", "rb") as f:
            return pickle.load(f)
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
    for item in userList.list():
        if item.check(username, password):
            init(item, x)
            return
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
    if not isinstance(userlist, UserList) or not isinstance(user, User):
        raise TypeError
    for item in userlist.list():
        if item.username == user.username:
            removeUser(userlist, item)
    try:
        os.mkdir(f"home/{user.username}")
    except FileExistsError:
        pass
    with open(f"home/{user.username}/init.d", "w") as f:
        f.write("terminal")
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
    print(f"{div2()}\nSetup Wizard\n{div2()}")
    username = input("Enter Your Username $")
    password = ""
    while password == "":
        password = getpass("Set A Password $")
        if password == "":
            print("Error: Cannot set blank password.")
    if password == "":
        password = None
    groupList = GroupList()
    g = groupList.byName("root")
    user = User(g, username, password)
    userList = UserList()
    userList = createUser(userList, user)
    saveUserList(userList)
    cls()
    div()
    print(f'Created user "{username}".')
    br()
    cls()
    if input("Set up autologin? [y/n] $").lower() == "y":
        saveAL(username)
        cls()
    div()
    print("Thank you for setting up Pythinux.")
    print("For an introduction to Pythinux, run the `welcome` command.")
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
        print(
            "Reinstall Pythinux from source:"
            "https://github.com/WinFan3672/Pythinux"
        )
        br()
    cdir = os.getcwd()
    global userList, groupList
    if loadUserList().users == []:
        setupWizard()
    userList = loadUserList()
    groupList = loadGroupList()
    global pdir
    global aliases
    aliases = loadAliases()
    pdir = dir()
    loginScreen(loadAL())

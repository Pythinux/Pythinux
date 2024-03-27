import os
import importlib
import zipfile
import traceback
import shutil
import sys
import configparser

pkm = load_program("pkm", currentUser, libMode=True, shell="installd")
shell = load_program("shell", currentUser, libMode=True)
libsemver = load_program("libsemver", currentUser, libMode=True)

class InstallError(Exception):
    pass

def getScripts(ini):
    scripts = []
    scripts.append(ini.get("Scripts", "Install", fallback=None))
    scripts.append(ini.get("Scripts", "Update", fallback=None))
    scripts.append(ini.get("Scripts", "Remove", fallback=None))
    return [x for x in scripts if x]

def installdBase(filename, yesMode=False):
    with zipfile.ZipFile(filename) as z:
        z.extract("program.ini", file.evalDir("/tmp", currentUser))

        ini = configparser.ConfigParser()
        ini.read(file.evalDir("/tmp/program.ini", currentUser))
        if not ini.has_section("Program"):
            raise InstallError("File program.ini in installer has no Program section")

        name = ini.get("Program", "name", fallback="[No program name]")
        version = ini.get("Program", "version", fallback="1.0.0")
        if not libsemver.check(version):
            raise InstallError("Defined version ({}) is not a semantic version (x.y.z)".format(version))

        author = ini.get("Program", "author", fallback="null")
        maintainer = ini.get("Program", "maintainer", fallback="null")
        date = ini.get("Program", "release", fallback="1 January 1970")
        deps = [x for x in ini.get("Program", "dependencies", fallback="").split("; ") if x]
        deps = [x for x in deps if x not in pkm.getPackageList()]
        conflicts = ini.get("Program", "conflicts", fallback="").split("; ")
        
        if ini.get("Program", "package") in pkm.getPackageList():
            return 2 # Package already exists

        if ini.has_section("Files"):
            files = dict(ini["Files"])
        else:
            files = {}
        folders = ini.get("Folders", "folders", fallback="").split("; ")
        
        if not yesMode:
            cls()
            div()
            print("Package: {}".format(ini.get("Program", "package")))
            print("Name: {}".format(name))
            print("Version: {}".format(version))
            print("Author: {}".format(author))
            print("Maintainer: {}".format(maintainer))
            print("Released: {}".format(date))
            div()
            inst = input("Install? [Y/n] $").lower()
            if inst == "n":
                return 1 # Action canceled
        currDep = 1
        for dep in deps:
            print("({}/{}) Installing '{}' (dependency of '{}')...".format(currDep, len(deps), dep, ini.get("Program", "package")))
            runCommand(currentUser, "pkm install -d {}".format(dep))
            currDep += 1
        for item in files:
            location = files[item]
            if location.startswith("@"):
                command = "{} {}".format(location[1:], file.evalDir("/tmp/{}".format(item), currentUser))
                z.extract(item, file.evalDir("/tmp", currentUser))
                runCommand(currentUser, command)
            else:
                with z.open(item) as zff:
                    with file.open(location, currentUser, "wb") as f:
                        f.write(zff.read())

        ignoredFolders = []
        for item in folders:
            directory = file.evalDir(item, currentUser)
            if not os.path.isdir(directory):
                os.mkdir(directory)
            else:
                ignoredFolders.append(directory)

        ini.set("Folders", "ignored", "; ".join(ignoredFolders))

        with file.open("/share/pkm/programs/{}".format(ini.get("Program", "package")), currentUser, "w") as p:
            ini.write(p)

        installScript = ini.get("Scripts", "Install", fallback=None)
        updateScript = ini.get("Scripts", "Update", fallback=None)
        removeScript = ini.get("Scripts", "Remove", fallback=None)
        if installScript:
            z.extract(installScript, file.evalDir("/tmp", currentUser))
            shell.runScript(currentUser, "/tmp/{}".format(installScript))
        if updateScript:
            z.extract(updateScript, file.evalDir("/share/pkm/scripts/update", currentUser))
        if removeScript:
            z.extract(removeScript, file.evalDir("/share/pkm/scripts/remove", currentUser))
            
    return 0

def installd(filename, yesMode=False):
    try:
        return installdBase(filename, yesMode)
    except:
        return -1

def main(args):
    if args:
        result = installd(" ".join(args))
        if result:
            print("ERROR: Exit code {} given. Check installd's manpage for more information.")
        else:
            print("Program successfully installed.")
    else:
        div()
        print("installd /path/to/program.szip4")
        div()
        print("Install an SZIP4 package.")
        div()

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
import importlib
import zipfile
import traceback
import shutil
import sys
import configparser

pkm = load_program("pkm", currentUser, libMode=True, shell="installd")
shell = load_program("shell", currentUser, libMode=True)
libsemver = load_program("libsemver", currentUser, libMode=True)
Version = load_program("version", currentUser, libMode=True)

class InstallError(Exception):
    pass

def getScripts(ini):
    assertTrue(isinstance(ini. configparser.ConfigParser), "Invalid config")
    scripts = []
    scripts.append(ini.get("Scripts", "Install", fallback=None))
    scripts.append(ini.get("Scripts", "Update", fallback=None))
    scripts.append(ini.get("Scripts", "Remove", fallback=None))
    return [x for x in scripts if x]

def installdBase(filename, yesMode=False, forceMode=False, depMode=False):
    assertTrue(isinstance(filename, str), "Filename must be a string")
    assertTrue(isinstance(yesMode, bool), "Invalid boolean flag")
    assertTrue(isinstance(forceMode, bool), "Invalid boolean flag")
    assertTrue(isinstance(depMode, bool), "Invalid boolean flag")
    with zipfile.ZipFile(filename) as z:
        z.extract("program.ini", file.evalDir("/tmp", currentUser))

        ini = configparser.ConfigParser()
        ini.read(file.evalDir("/tmp/program.ini", currentUser))
        if not ini.has_section("Program"):
            raise InstallError("File program.ini in installer has no Program section")

        name = ini.get("Program", "name", fallback="[No program name]")
        version = ini.get("Program", "version", fallback="1.0.0")
        try:
            if not libsemver.check(version):
                raise InstallError("Defined version ({}) is not a semantic version (x.y.z)".format(version))
        except libsemver.SemanticVersionError:
            return 5

        author = ini.get("Program", "author", fallback="null")
        maintainer = ini.get("Program", "maintainer", fallback="null")
        date = ini.get("Program", "release", fallback="1 January 1970")
        deps = [x for x in ini.get("Program", "dependencies", fallback="").split("; ") if x]
        deps = [x for x in deps if x not in pkm.getPackageList()]
        conflicts = ini.get("Program", "conflicts", fallback="").split("; ")
        replaces = ini.get("Program", "replaces", fallback=None)
        
        if ini.get("Program", "package") in pkm.getPackageList() and not forceMode:
            return 2 # Package already exists

        if replaces and replaces in pkm.getPackageList():
            if forceMode or yesMode or depMode:
                choice = "y"
            else:
                choice = input("This package replaces the installed '{}'. Do you want to remove it and install this one? [Y/n]").lower()
            if choice == "y":
                pkm.removePackage(replaces)
            else:
                return 1 # Action canceled

        if ini.has_section("Files"):
            files = dict(ini["Files"])
        else:
            files = {}
        folders = ini.get("Folders", "folders", fallback="").split("; ")
        
        min_version = ini.getfloat("Program", "min_version", fallback=3.0)
        max_version = ini.getfloat("Program", "max_version", fallback=4.0)
    
        conflictingPackages = [x for x in pkm.getPackageList() if x in conflicts]
        if conflictingPackages:
            for c in conflictingPackages:
                print("ERROR: This package conflicts with the installed '{}' package.".format(c))
            return -1

        if Version.getfloat() < min_version:
            return 3
        if Version.getfloat() > max_version:
            return 4

        if not yesMode:
            cls()
            pkm.dispInfo(ini)
            inst = input("Install? [Y/n] $").lower()
            if inst == "n":
                return 1 # Action canceled
        if not depMode:
            print("(1/5) Installing dependencies...")
        currDep = 1
        for dep in deps:
            if not depMode:
                print("==> ({}/{}) Installing '{}' (dependency of '{}')...".format(currDep, len(deps), dep, ini.get("Program", "package")))
            runCommand(currentUser, "pkm install -d {}".format(dep))
            currDep += 1
        
        if not depMode:
            print("(2/5) Creating folders...")
        ignoredFolders = []
        for item in folders:
            if not depMode:
                print("==> {}".format(item))
            directory = file.evalDir(item, currentUser)
            if not os.path.isdir(directory):
                os.mkdir(directory)
            else:
                ignoredFolders.append(directory)
        if not depMode:
            print("(3/5) Copying and parsing files...")
        for item in files:
            if not depMode:
                print("==> {}".format(item))
            location = files[item]
            if location.startswith("@"):
                command = "{} {}".format(location[1:], file.evalDir("/tmp/{}".format(item), currentUser))
                z.extract(item, file.evalDir("/tmp", currentUser))
                runCommand(currentUser, command)
            else:
                with z.open(item) as zff:
                    with file.open(location, currentUser, "wb") as f:
                        f.write(zff.read())

        if not ini.has_section("Folders"):
            ini.add_section("Folders")
        ini.set("Folders", "ignored", "; ".join(ignoredFolders))
        if not depMode:
            print("(4/5) Registering program data...")

        with file.open("/share/pkm/programs/{}".format(ini.get("Program", "package")), currentUser, "w") as p:
            ini.write(p)
        if not depMode:
            print("(5/5) Parsing scripts...")
        installScript = ini.get("Scripts", "Install", fallback=None)
        updateScript = ini.get("Scripts", "Update", fallback=None)
        removeScript = ini.get("Scripts", "Remove", fallback=None)
        if installScript:
            if not depMode:
                print("==> Running install script...")
            z.extract(installScript, file.evalDir("/tmp", currentUser))
            shell.runScript(currentUser, "/tmp/{}".format(installScript))
        if updateScript:
            if not depMode:
                print("==> Saving update script...")
            z.extract(updateScript, file.evalDir("/share/pkm/scripts/update", currentUser))
        if removeScript:
            if not depMode:
                print("==> Saving removal script...")
            z.extract(removeScript, file.evalDir("/share/pkm/scripts/remove", currentUser))
            
    return 0

def installd(*args, **kwargs):
    return installdBase(*args, **kwargs)

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

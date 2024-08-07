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
import shutil
import configparser
import urllib.request
import traceback
import zipfile
import warnings

disallowInstalld = getTerm() == "installd"

if not disallowInstalld:
    installd = load_program("installd", currentUser, libMode=True)
libsemver = load_program("libsemver", currentUser, libMode=True)
libconfig = load_program("libconfig", currentUser, libMode=True)
libupgrade = load_program("libupgrade", currentUser, libMode=True)
shell = load_program("shell", currentUser, libMode=True)

global config, version

config = libconfig.load("/config/pkm.ini", {
    "repos": {
        "core": "https://codeberg.org/Pythinux/Core/raw/branch/main/db.ini",
        "community": "https://codeberg.org/Pythinux/Community/raw/branch/main/db.ini",
    }
})

# config = configparser.ConfigParser()
# if not config.has_section("repos"):
#     config.add_section("repos")
#     config.set("repos", "core", "")
#     config.set("repos", "community", "")

version = [4, 0, 0]

def downloadFile(url, fileName):
    """
    Download a remote HTTP resource and save it to a file.
    """
    assertTrue(isinstance(url, str), "URL must be a string")
    assertTrue(isinstance(fileName, str), "Filename must be a string")

    urllib.request.urlretrieve(url, file.evalDir(fileName, currentUser))

def sectionToDict(config, section):
    """
    Convert a ConfigParser section to a dictionary.
    
    Args:
    - config: ConfigParser object
    - section: Name of the section
    
    Returns:
    - dict containing the key-value pairs of the section
    """
    assertTrue(isinstance(config, configparser.ConfigParser), "Not a valid ConfigParser")
    assertTrue(isinstance(section, str), "Section name must be a string")

    dict_section = {}
    options = config.options(section)
    for option in options:
        dict_section[option] = config.get(section, option)
    return dict_section

def getLocalPackageData():
    """
    Returns package data as a dict in the format <package name>: <ConfigParser object>
    """
    data = {}
    for package in getPackageList():
        ini = configparser.ConfigParser()
        ini.read(file.evalDir("/share/pkm/programs/{}".format(package), currentUser))
        data[package] = ini
    return data

def getRemotePackageData(offline=True, silent=False):
    """
    This function returns package data as a dict in the format <package name>: <ConfigParser object>
    """
    assertTrue(isinstance(offline, bool), "Boolean flag not a boolean")
    assertTrue(isinstance(silent, bool), "Boolean flag not a boolean")

    repos = sectionToDict(config, "repos")
    packageData = configparser.ConfigParser()
    if offline:
        packageData.read(file.evalDir("config/pkmdata.ini", currentUser))
    else:
        if not silent:
            print("Updating database...")
        for repo in repos:
            if not silent:
                print("Downloading '{}'...".format(repo))
            downloadFile(repos[repo], "/tmp/repo")
            packageData.read("tmp/repo")
    with file.open("/config/pkmdata.ini", currentUser, "w") as f:
        packageData.write(f)
    if not silent and not offline:
        print("Successfully updated database.")
    return packageData

def getPackageList():
    """
    Returns a list of installed packages.
    """
    return os.listdir(file.evalDir("/share/pkm/programs/", currentUser))

def getRemotePackageList():
    """
    Returns a list of remote packages.
    """
    return [x for x in getRemotePackageData(silent=True).keys() if x != "DEFAULT"]
def saveConfig():
    """
    Call this function to ensure the config is saved.
    """
    libconfig.save(config, "/config/pkm.ini")

def loadConfig():
    """
    Call this function to update `config` by reading the pkm.ini file.
    """
    config.read(file.evalDir("/config/pkm.ini", currentUser))

def installPackage(package, yesMode=False, depMode=False, forceMode=False):
    """
    Install a package.
    Arguments:
        package: package name
        yesMode: passed to installd.installd()
        depMode: passed to installd.installd()
        forceMode: passed to installd.installd()
    """
    assertTrue(isinstance(package, str), "Package name must be a string")
    assertTrue(isinstance(yesMode, bool), "Invalid boolean flag")
    assertTrue(isinstance(depMode, bool), "Invalid boolean flag")
    assertTrue(isinstance(forceMode, bool), "Invalid boolean flag")

    clearTemp(currentUser)
    isData = bool(getRemotePackageData().sections())
    data = getRemotePackageData(isData)
    url = data.get(package, "url", fallback=None)
    if url:
        downloadFile(url, "tmp/program.szip4")
        result = dispErrInfo(installd.installd(file.evalDir("/tmp/program.szip4", currentUser), yesMode, forceMode, depMode), package, depMode)
        if result:
            print(result)
    else:
        print("ERROR: Package not found.")

def installPackageFromRepo(repo, package, yesMode=False, forceMode=False):
    assertTrue(isinstance(repo, str), "Repo name must be a string")
    assertTrue(isinstance(package, str), "Package name must be a string")
    assertTrue(isinstance(yesMode, bool), "Invalid boolean flag")
    assertTrue(isinstance(forceMode, bool), "Invalid boolean flag")

    downloadFile(config.get("repos", repo), file.evalDir("/tmp/pkmdata.ini", currentUser))
    conf = configparser.ConfigParser()
    conf.read(file.evalDir("/tmp/pkmdata.ini", currentUser))
    url = conf.get(package, "url")
    if url:
        downloadFile(url, file.evalDir("/tmp/pkg.szip4", currentUser))
        return installd.installd(file.evalDir("/tmp/pkg.szip4", currentUser), yesMode, forceMode)
    else:
        print("ERROR: Invalid URL.")
        return -1

def getDeps(pkg):
    """
    Returns a list of dependencies for a local package.
    """
    assertTrue(isinstance(pkg, str), "Package name must be a string")

    config = configparser.ConfigParser()
    config.read(file.evalDir("/share/pkm/programs/{}".format(pkg), currentUser))
    if not config.has_section("Program"):
        warnings.warn("removePackage(): invalid package file specified")
        return []
    deps = config.get("Program", "dependencies", fallback=None)
    deps = deps.split("; ") if deps else []
    return deps   


def removePackage(package, force=False):
    """
    Uninstall a package.
    """
    assertTrue(isinstance(package, str), "Package name must be a string")
    assertTrue(isinstance(force, bool), "Invalid boolean flag")
    if not package in getPackageList():
        print("ERROR: Invalid package.")
        return 1
    foundDeps = False

    for pkg in getPackageList():
        if package in getDeps(pkg) and not force:
            print("ERROR: '{}' depends on '{}' and cannot be removed".format(pkg, package))
            foundDeps = True
    if foundDeps:
        return 1

    ini = configparser.ConfigParser()
    ini.read(file.evalDir("/share/pkm/programs/{}".format(package), currentUser))
    if ini.has_section("Files"):
        files = dict([x for x in ini.items("Files") if "@" not in x[1]])
    else:
        files = []
    if ini.has_option("Folders", "folders"):
        folders = [file.evalDir(x, currentUser) for x in ini.get("Folders", "folders").split("; ")]
        ignored = ini.get("Folders", "ignored").split("; ")
    else:
        folders = []
    for x in files:
        fn = file.evalDir(x, currentUser)
        if os.path.isfile(fn):
            os.remove(fn)
    
    for folder in [x for x in folders if x not in ignored]:
        if os.path.isdir(folder):
            shutil.rmtree(folder)

    os.remove(file.evalDir("/share/pkm/programs/{}".format(package), currentUser))
    print("Successfully removed '{}'.".format(package))
    return 0

def searchForPackages(term):
    """
    Returns a list of REMOTE packages where the package name contains term.
    Returns a list of packages if term == 'ALL'.
    """
    assertTrue(isinstance(term, str), "Search term must be a string")
    if term == "ALL":
        return getRemotePackageData(False,True).sections()
    else:
        return [x for x in getRemotePackageData(False, True) if term in x]

def dispInfo(ini, showInstalledState=False):
    """
    Displays package info.
    ini is a configparser.ConfigParser object.
    """
    assertTrue(isinstance(ini, configparser.ConfigParser), "Invalid config")
    assertTrue(isinstance(showInstalledState, bool), "Invalid boolean flag")
    deps = ini.get("Programs", "dependencies", fallback="None")
    conflicts = ini.get("Program", "conflicts", fallback="")
    conflicts = conflicts if conflicts else "None"
    div()
    print("Name: {}".format(ini.get("Program", "name", fallback="Unknown")))
    print("Version: {}".format(ini.get("Program", "version", fallback="1.0.0")))
    print("Description: {}".format(ini.get("Program", "description", fallback="None")))
    print("Author: {}".format(ini.get("Program", "author", fallback="Unknown")))
    print("Maintainer: {}".format(ini.get("Program", "maintainer", fallback="Unknown")))
    print("Min. Pythinux Version: {}".format(ini.get("Program", "min_version", fallback="3.0")))
    print("Dependencies: {}".format(deps))
    print("Conflicts: {}".format(conflicts))
    if showInstalledState:
        print("Installed: {}".format("Yes" if ini.get("Program", "package") in getPackageList() else "No"))
    div()

def dispErrInfo(result, package, depMode=False):
    """
    Turns an error code into something more useful.
    """
    assertTrue(isinstance(result, int), "Invalid integer")
    assertTrue(isinstance(package, str), "Package name must be a string")
    assertTrue(isinstance(depMode, bool), "Invalid boolean flag")
    if result == 1:
        return "ERROR: User action canceled."
    elif result == 0 and depMode:
        return
    elif result == 0:
        return "Successfully installed '{}'.".format(package)
    elif result == 2:
        return "ERROR: Package '{}' is already installed.\nERROR: To rectify this, run 'pkm remove {}' and try again.".format(package, package)
    elif result == 3:
        return "ERROR: Your Pythinux version is too old to install this software.\nERROR: To fix this, update Pythinux."
    elif result == 4:
        return "ERROR: This package is for an older Pythinux version."
    elif result == 5:
        return "ERROR: Invalid semantic version for package '{}'.".format(package)
    elif result == -1:
        return
    else:
        return "Unknown Exit Code: {}".format(result)
def main(args):
    loadConfig()
    saveConfig()
    if args == ["update"]:
        getRemotePackageData(False)
    elif args in [["version"], ["ver"], ["v"]]:
        div()
        print("PKM {}".format(".".join([str(x) for x in version])))
        div()
        print("PKM (c) Pythinux team 2022-2024, some rights reserved.")
        div()
    elif args == ["repo"]:
        div()
        print("pkm repo [arg]")
        div()
        print("Manage repositories.")
        div()
        print("Positional arguments:")
        print("    add <name> <url>: add a repository")
        print("    list: lists all repositories")
        print("    rm <name>: remove a repository")
        div()
    elif args in [["repo", "list"], ["repo", "ls"]]:
        repos = sectionToDict(config, "repos")
        div()
        for repo in repos:
            print("{} --> {}".format(repo, repos[repo]))
        div()
    elif args == ["repo", "add"]:
        div()
        print("pkm repo add <name> <url")
        div()
        print("Adds a repository to PKM's database.")
        div()
    elif "repo" in args and "add" in args and len(args) == 4:
        args.remove("repo")
        args.remove("add")
        name = args[0]
        url = args[1]
        loadConfig()
        config.set("repos", name, url)
        saveConfig()
        getRemotePackageData(False)
    elif args == ["all"]:
        packages = getRemotePackageData(False, True)
        for package in packages.sections():
            div()
            print("{} {}".format(package, packages.get(package, "version")))
            print("    {}".format(packages.get(package, "name")))
            print("    {}".format(packages.get(package, "description")))
        div()
        if len(packages.sections()) == 0:
            print("ERROR: No packages found.")
            div()
    elif args == ["repo", "rm"]:
        div()
        print("pkm repo rm <name>")
        div()
        print("Remove a repository from PKM's repo list.")
        div()
    elif "repo" in args and "rm" in args and len(args) == 3:
        args.remove("repo")
        args.remove("rm")
        name = args[0]
        loadConfig()
        config.remove_option("repos", name)
        saveConfig()
        print("Successfully removed repository '{}'.".format(name))
    elif args == ["allc"]:
        packages = getRemotePackageData(False, True)
        print("\n".join(packages.sections()))
    elif args == ["install"]:
        div()
        print("pkm install <package(s)> [-y]")
        div()
        print("Downloads a package file and installs it.")
        div()
    elif "install" in args:
        args.remove("install")
        if "-y" in args:
            yesMode = True
            args.remove("-y")
        else:
            yesMode = False
        if "-d" in args:
            depMode = True
            yesMode = True
            args.remove("-d")
        else:
            depMode = False
        for arg in args:
            installPackage(arg, yesMode, depMode=depMode)
    elif args == ["list"]:
        ls = sorted(getPackageList())
        div()
        if ls:
            print("\n".join(ls))
        else:
            print("ERROR: No packages installed.")
        div()
    elif args == ["remove"]:
        div()
        print("pkm remove <package>")
        div()
        print("Remove a package.")
        div()
    elif "remove" in args and len(args) == 2:
        args.remove("remove")
        removePackage(args[0])
    elif args == ["clear", "-y"]:
        while getPackageList():
            for program in getPackageList():
                removePackage(program)
    elif args == ["clear"]:
        print("ERROR: This will remove ALL of your packages.")
        print("ERROR: Run `pkm clear -y` to confirm.")
    elif args == ["search"]:
        div()
        print("pkm search <term>")
        div()
        print("Find a package to install.")
        div()
    elif "search" in args:
        args.remove("search")
        results = searchForPackages(" ".join(args))
        data = getRemotePackageData()
        div()
        for res in results:
            print("{} {}".format(res, data.get(res, "version")))
            print("    {}".format(data.get(res, "description")))
        if not results:
            print("No packages found.")
        div()
    elif args == ["batch"]:
        div()
        print("pkm batch <repository>")
        div()
        print("Install all packages in a particular repository.")
        print("WARNING: This can install a LOT of packages.")
        div()
    elif "batch" in args and len(args) == 2:
        args.remove("batch")
        repo = config.get("repos", args[0])
        clearTemp(currentUser)
        downloadFile(repo, "/tmp/db.ini")
        ini = configparser.ConfigParser()
        ini.read(file.evalDir("/tmp/db.ini", currentUser))
        for package in ini.sections():
            clearTemp(currentUser)
            downloadFile(ini.get(package, "url"), "/tmp/package.szip4")
            exitCode = installd.installd(file.evalDir("/tmp/package.szip4", currentUser), True)
            if exitCode:
                print("ERROR: installd returned exit code {} for package '{}'. Run `man installd` for more info.".format(exitCode, package))
    elif args == ["info"]:
        div()
        print("pkm info <package>")
        div()
        print("Displays info about a package.")
        div()
    elif "info" in args and len(args) == 2:
        args.remove("info")
        if args[0] in getPackageList():
            ini = configparser.ConfigParser()
            ini.read(file.evalDir("/share/pkm/programs/{}".format(args[0]), currentUser))
            dispInfo(ini, True)
        elif args[0] in getRemotePackageData(False, True).sections():
            data = getRemotePackageData()
            downloadFile(data.get(args[0], "url"), "/tmp/program.szip4")
            with zipfile.ZipFile(file.evalDir("/tmp/program.szip4", currentUser)) as f:
                f.extract("program.ini", file.evalDir("/tmp", currentUser))
            ini = configparser.ConfigParser()
            ini.read(file.evalDir("/tmp/program.ini", currentUser))
            dispInfo(ini, True)
        else:
            print("ERROR: Package not installed.")
    elif args == ["upgrade"]:
        print("Upgrading...")
        data = getRemotePackageData(False, True)
        packages = getPackageList()
        upgrades = []
        for package in packages:
            remote = data.get(package, "version", fallback="1.0.0")
            ini = getLocalPackageData()[package]
            local = ini.get("Program", "version", fallback = "1.0.0-1")
            try:
                if libsemver.compare(local, remote) == -1:
                    upgrades.append(package)
            except libsemver.SemanticVersionError:
                print("ERROR: `{}` has an invalid semantic version. Cannot check for upgrade.".format(package))
        i = 1
        for upgrade in upgrades:
            print("({}/{}) Upgrading '{}'...".format(i, len(upgrades), upgrade))
            installPackage(upgrade, True, False, True)
            i += 1
        if upgrades:
            print("Upgraded all packages.")
        else:
            print("No packages to upgrade.")
    elif args == ["from"]:
        div()
        print("pkm from <repository> <package>")
        div()
        print("Install a package from a specific repository.")
        div()
    elif "from" in args and len(args) == 3:
        args.remove("from")
        result = dispErrInfo(installPackageFromRepo(args[0], args[1]), args[1])
        if result:
            print(result)
    elif args == ["reinstall"]:
        div()
        print("pkm reinstall <package>")
        div()
        print("Uninstall and re-install a package.")
        div()
    elif "reinstall" in args and len(args) == 2:
        args.remove("reinstall")
        status = removePackage(args[0], force=True)
        if status == 0:
            installPackage(args[0], yesMode=True)
    elif args == ["dist-upgrade"]:
        libupgrade.installUpgrades()
    else:
        div()
        print("pkm [args]")
        div()
        print("Pythinux package manager.")
        div()
        print("Positional arguments:")
        print("    all: lists all installable packages")
        print("    allc: lists all installable packages [compact]")
        print("    batch <repository>: installs every package in a particular repository")
        print("    clear: removes all installed packages")
        print("    dist-upgrade: upgrades Pythinux version in-placte")
        print("    from <repository> <package>: installs a package from a specific repository")
        print("    info <package>: prints information about an installed package")
        print("    install <package>: installs a package")
        print("    list: lists all installed programs")
        print("    remove <package>: remove a package")
        print("    repo: manages repositories")
        print("    reinstall <package>: uninstall and then install a package")
        print("    search <package name>: searches for a package by name")
        print("    update: updates remote package list")
        print("    upgrade: upgrades all installed packages")
        print("    version: displays version information")
        div()

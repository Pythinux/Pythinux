"""
PKM 4.x

Package manager

API:
    getPackageData()
        Returns a dict with package data.
    saveConfig()
        Saves the config to /config/pkm.ini
    loadConfig()
        Refreshes the config from /config/pkm.ini
    
"""

import configparser
import urllib.request
import traceback
installd = load_program("install", currentUser, libMode=True)

global config, version

config = configparser.ConfigParser()
config.add_section("repos")
config.set("repos", "core", "https://codeberg.org/Pythinux/Core/raw/branch/main/db.ini")

applications = configparser.ConfigParser()
# config.set("repos", "community", "https://codeberg.org/Pythinux/Community/raw/branch/main/db.ini")

version = [4, 0, 0]

def downloadFile(url, fileName):
    """
    Download a remote HTTP resource and save it to a file.
    """
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
    dict_section = {}
    options = config.options(section)
    for option in options:
        dict_section[option] = config.get(section, option)
    return dict_section

def getPackageData(offline=True):
    """
    This function returns package data as a dict
    """
    repos = sectionToDict(config, "repos")
    packageData = configparser.ConfigParser()
    if offline:
        packageData.read(file.evalDir("config/pkmdata.ini", currentUser))
    else:
        print("Updating database...")
        for repo in repos:
            print("Downloading '{}'...".format(repo))
            downloadFile(repos[repo], "/tmp/repo")
            packageData.read("tmp/repo")
    with open(file.evalDir("/config/pkmdata.ini", currentUser), "w") as f:
        packageData.write(f)
    print("Successfully updated database.")
    return packageData
def saveConfig():
    with open(file.evalDir("/config/pkm.ini", currentUser), "w") as f:
        config.write(f)

def loadConfig():
    config.read(file.evalDir("/config/pkm.ini", currentUser))

def registerApp(app):
    data = getPackageData()
    applications.add_section(app)

def main(args):
    loadConfig()
    saveConfig()
    if args == ["update"]:
        getPackageData(False)
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
        # print("    add <name> <url>: add a repository")
        print("    list: lists all repositories")
        # print("    remove <name>: remove a repository")
        div()
    elif args in [["repo", "list"], ["repo", "ls"]]:
        repos = sectionToDict(config, "repos")
        div()
        for repo in repos:
            print("{} --> {}".format(repo, repos[repo]))
        div()
    else:
        div()
        print("pkm [args]")
        div()
        print("Pythinux package manager.")
        div()
        print("Positional arguments:")
        # print("    install <package>: installs a package")
        # print("    search <package name>: searches for a package by name")
        # print("    remove <package>: remove a package")
        # print("    clear: removes all installed packages")
        print("    update: updates the database")
        # print("    upgrade: upgrades all installed packages")
        # print("    list: lists all installed programs")
        # print("    info <package>: prints information about an installed package")
        # print("    rinfo <package>: prints information about an installable package")
        # print("    all: lists all installable packages")
        # print("    allc: lists all installable packages [compact]")
        print("    repo: manages repositories")
        # print("    batch <database>: installs every package in a particular database")
        # print("    from <database> <package>: installs a package from a specific database")
        print("    version: states the version of PKM")
        div()

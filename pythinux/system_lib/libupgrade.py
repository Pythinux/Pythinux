"""
libupgrade - Backend for Pythinux Update Framework
"""

import urllib.request
import zipfile
libconfig = load_program("libconfig", currentUser, libMode=True)
libsemver = load_program("libsemver", currentUser, libMode=True)

REPO = "https://codeberg.org/Pythinux/Update/raw/branch/main/repo.ini"
VERSION = ".".join([str(x) for x in version]) + "-1"

def downloadFile(url, fileName):
    """
    Download a remote HTTP resource and save it to a file.
    """
    urllib.request.urlretrieve(url, file.evalDir(fileName, currentUser))

def checkForNewVersions():
    clearTemp(currentUser)
    downloadFile(REPO, "/tmp/repo.ini")
    ini = libconfig.load("/tmp/repo.ini")
    return [x for x in ini.sections() if libsemver.compare(VERSION, x) == -1], ini

def installUpgrades():
    upgrades, ini = checkForNewVersions()
    if not upgrades:
        print("Your system is up-to-date.")
        return
    i = 1
    clearTemp(currentUser)
    for upgrade in upgrades:
        url = ini.get(upgrade, "url")
        downloadFile(url, "/tmp/update.puf4")
        with zipfile.ZipFile(file.evalDir("/tmp/update.puf4", currentUser)) as zf:
            os.chdir(file.evalDir("/", currentUser))
            os.chdir("..")
            zf.extractall()

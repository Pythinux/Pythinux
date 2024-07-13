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
    assertTrue(isinstance(url, str))
    assertTrue(isinstance(fileName, str))
    urllib.request.urlretrieve(url, file.evalDir(fileName, currentUser))

def checkForNewVersions():
    clearTemp(currentUser)
    downloadFile(REPO, "/tmp/repo.ini")
    ini = libconfig.load("/tmp/repo.ini")
    return [x for x in ini.sections() if libsemver.compare(VERSION, x) == -1], ini

def installUpgrades():
    print("Checking for updates...")
    upgrades, ini = checkForNewVersions()
    if not upgrades:
        print("Your system is up-to-date.")
        return
    i = 1
    clearTemp(currentUser)
    for upgrade in upgrades:
        print("Installing {}...".format(upgrade))
        url = ini.get(upgrade, "url")
        downloadFile(url, "/tmp/update.puf4")
        with zipfile.ZipFile(file.evalDir("/tmp/update.puf4", currentUser)) as zf:
            os.chdir(file.evalDir("/", currentUser))
            os.chdir("..")
            zf.extractall()
    print("Success! Restart Pythinux for all changes to take effect.")

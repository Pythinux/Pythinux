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
import re

class SemanticVersionError(Exception):
    pass

def check(version):
    """
    Checks if a string is in the format x.y.z-a, AKA semantic versioning.
    """
    assertTrue(isinstance(version, str))
    pattern = r'^\d+\.\d+\.\d+-\d+$'
    return bool(re.match(pattern, version))
def compare(a, b):
    """
    Compares semantic versions.
    Returns 1 if a is a higher version than b, -1 if b is a higher version than a, and 0 if both are the same.
    """
    assertTrue(isinstance(a, str))
    assertTrue(isinstance(b, str))

    def normalize(version):
        version = version.replace("-", ".")
        return [int(x) for x in version.split(".")]

    if not check(a) or not check(b):
        raise SemanticVersionError("Strings must be in the format x.y.z-a")

    version_a = normalize(a)
    version_b = normalize(b)

    for i in range(4):
        if version_a[i] < version_b[i]:
            return -1
        elif version_a[i] > version_b[i]:
            return 1

    return 0


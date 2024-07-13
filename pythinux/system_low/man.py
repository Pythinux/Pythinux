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

def dirTree():
    manuals = []
    path = "man/"
    for root, dirs, files in os.walk(path):
        for file in files:
            manuals.append(file)
    return files
def main(args):
    if args == ["/"]:
        div()
        print("\n".join(sorted(dirTree())))
        div()
    else:
        if args:
            manual = "man/" + " ".join(args)
        else:
            manual = "man/man"
        try:
            with file.open(manual, currentUser) as f:
                cls()
                div()
                print(f.read())
                br()
                cls()
        except FileNotFoundError:
            print("ERROR: Manual `{}` is not valid.".format(manual))

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

libargs = load_program("libargs", currentUser, libMode=True)

parser = libargs.ArgumentParser("debugmgr", description="Manage debuggers")
subs = parser.add_subparsers(dest="cmd", help="Sub-command help")

parser_list = subs.add_parser("list", help="Lists debuggers")

parser_add = subs.add_parser("add", help="Adds a debugger")
parser_add.add_argument("debugger", help="Debugger to add")

parser_remove = subs.add_parser("remove", help="Remove a debugger")
parser_remove.add_argument("debugger", help="Debugger to remove")

args = parser.parse_args(args)


def main(args):
    if args.cmd == "list":
        div()
        for debugger in debug.list_debuggers(currentUser):
            print("{}{}".format(debugger, "*" if debugger in debug.system else ""))
        div()
    elif args.cmd == "add":
        debug.grant_debugging(args.debugger, currentUser)
        debug.cleanup(currentUser)
    elif args.cmd == "remove":
        debug.revoke_debugging(args.debugger, currentUser)
        debug.cleanup(currentUser)
    else:
        parser.print_help()

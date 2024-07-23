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

libtime = load_program("libtime", currentUser, libMode=True)

class Log:
    def __init__(self, filename, display=True, show_date=False):
        assertTrue(isinstance(filename, str))
        assertTrue(isinstance(display, bool))
        assertTrue(isinstance(show_date, bool))

        self.filename = filename
        self.logs = []
        self.display = display
        self.show_date = show_date
        self.load()

    def log(self, text, log_type="info"):
        assertTrue(isinstance(text, str))
        assertTrue(isinstance(log_type, str))

        log_text = "[{}{}] {}".format(log_type, "@{}".format(libtime.datetime()) if self.show_date else "", text)
        self.logs.append(log_text)
        if self.display:
            print(log_text)
        self.save()
    def load(self):
        if os.path.isfile(file.evalDir(self.filename, currentUser)):
            with file.open(self.filename, currentUser) as f:
                self.logs = f.read().split("\n")
    def save(self):
        with file.open(self.filename, currentUser, "w") as f:
            f.write("\n".join(self.logs))


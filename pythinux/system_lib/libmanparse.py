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

man = load_program("man", currentUser, libMode=True)

class Manpage:
    """
    Manpage class. Contains sections, which contain elements.
    There are three Section classes - Section, SubSection, and SubSubSection.
    """
    def __init__(self, name):
        self.name = name
        self.sections = []
    def flatten(self):
        """
        Returns each Section and Element in the Manpage as a flat list.
        """
        sections = []
        for section in self.sections:
            sections.append(section)
            sections += section.elements
        return sections

class Element:
    """
    An element is essentially a line of what isn't text.
    """
    def __init__(self, value):
        self.value = value

class Section:
    """
    A manpage section. Each section contains elements.
    """
    def __init__(self, name):
        self.name = name
        self.elements = []
        self.lines = ""
    def add(self, line):
        self.lines += line + "\n"
    def zip(self):
        self.elements.append(Element(self.lines))
        self.lines = ""

class SubSection(Section):
    pass

class SubSubSection(Section):
    pass

def getManpageText(manpage):
    """
    Gets the text of a manpage.
    """
    with file.open("/man/{}".format(manpage), currentUser) as f:
        return f.read().rstrip("\n").replace("    ", "\t")

def parseManpage(manpage):
    """
    Converts a manpage file into a Manpage class which can be used in parsing.
    """
    mp = Manpage(manpage)
    text = getManpageText(manpage).split("\n")
    current = None
    for line in text:
        if line.startswith("\t\t") and line.isupper():
            if current:
                current.zip()
                mp.sections.append(current)
            current = SubSubSection(line.lstrip().replace("\t\t", "", 1))
        elif line.startswith("\t") and line.isupper():
            if current:
                current.zip()
                mp.sections.append(current)
            current = SubSection(line.lstrip().replace("\t", "", 1))
        elif line.isupper():
            if current:
                current.zip()
                mp.sections.append(current)
            current = Section(line)
        else:
            current.add(line.replace("\t\t", "", 1).replace("\t", "", 1))
    return mp

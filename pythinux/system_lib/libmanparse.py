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

class Element:
    """
    Base class for an element.
    """
    def __init__(self, value):
        self.value = value

class Section:
    """
    A manpage section. Each section contains sections and elements.
    """
    def __init__(self, name, elements=[]):
        self.name = name
        self.elements = elements

class Manpage:
    def __init__(self, name):
        self.name = name
        self.sections = []

# def parseDocument(document):
#     parsedStructure = []
#     currentHeading = None
#     currentSubheading = None
#     currentIndentLevel = 0
#     
#     for line in document:
#         if line.strip() == "":
#             continue
#         
#         # Calculate the current indentation level
#         indentLevel = len(line) - len(line.lstrip())
#         
#         # Remove leading and trailing whitespace
#         content = line.strip()
#         
#         if indentLevel == 0:
#             # This line is a top-level heading
#             currentHeading = content
#             currentSubheading = None
#             currentIndentLevel = 0
#             parsedStructure.append((currentHeading, []))
#         
#         elif indentLevel == currentIndentLevel + 4:
#             # This line is a subheading
#             currentSubheading = content
#             parsedStructure[-1][1].append((currentSubheading, []))
#             currentIndentLevel += 4
#         
#         elif indentLevel > currentIndentLevel:
#             # This line is a sub-subheading, etc. (indentation must be consistent)
#             currentSubheading = content
#             parsedStructure[-1][1][-1][1].append((currentSubheading, []))
#             currentIndentLevel = indentLevel
#         
#         else:
#             # Treat as text under the current subheading
#             if currentSubheading is not None:
#                 parsedStructure[-1][1][-1][1].append(content)
#     
#     return parsedStructure
#
#
def getManpageText(manpage):
    """
    Returns the contents of a manpage.
    """
    with file.open("/man/{}".format(manpage), currentUser) as f:
        return f.read().rstrip("\n")

    return parsedData

# def countIndentation(line):
#     count = 0
#     for char in line:
#         if char == ' ':
#             count += 1
#         else:
#             break
#     return count
#
# def transformToDictionary(parsedStructure):
#     transformedDict = {}
#     
#     for heading, subheadings in parsedStructure:
#         transformedDict[heading] = {}
#         for subheading, texts in subheadings:
#             transformedDict[heading][subheading] = texts
#     
#     return transformedDict
#
# def handleDictionary(dictionary):
#     pprint(dictionary)
#     return dictionary

def parseSections(lines, indentLevel=0):
    sections = []
    while lines:
        line = lines.pop(0)
        if line.strip():  # Non-empty line
            sectionName = line.strip()
            section = {'name': sectionName, 'subsections': []}
            # Check for nested sections
            nextIndentLevel = indentLevel + 1
            while lines and lines[0].startswith(' ' * (nextIndentLevel * 4)):
                subsections = parseSections(lines, nextIndentLevel)
                section['subsections'].append(subsections)
            sections.append(section)
    return sections

def parseManpage(manpage):
    """
    Parses a manpage and returns a Manpage with its contents.
    """
    text = getManpageText(manpage)
    return parseSections(text.split("\n"))

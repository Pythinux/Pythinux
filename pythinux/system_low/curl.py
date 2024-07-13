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
import urllib.error
import urllib.request

class CurlException(Exception):
    pass

def curl(url, character_set="utf-8"):
    assertTrue(isinstance(url, str))
    assertTrue(isinstance(character_set, str))
    try:
        request = urllib.request.urlopen(url)
        if request.status == 200:
            charset = request.headers.get_content_charset()
            return request.read().decode(charset if charset else character_set)
        else:
            raise CurlException("HTTP Error {}".format(request.status))
    except urllib.error.URLError as e:
        raise CurlException("Failed to connect to server: {}".format(e.reason))
    except urllib.error.HTTPError as e:
        raise CurlException("HTTP error {}: {}".format(e.code, e.reason))

def main(args):
    if len(args) == 1:
        print(curl(args[0]))
    else:
        div()
        print("curl <url>")
        div()
        print("Downloads a remote file and displays it.")
        div()

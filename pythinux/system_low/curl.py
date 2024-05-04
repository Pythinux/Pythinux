import urllib.error
import urllib.request

class CurlException(Exception):
    pass

def curl(url, character_set="utf-8"):
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

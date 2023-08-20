import sys
import requests
import markdown
import pickle
import toml
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

global http_status_codes
http_status_codes = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    226: "IM Used",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Content Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    421: "Misdirected Request",
    422: "Unprocessable Content",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    511: "Network Authentication Required"
}

def clearLayout(layout):
    while layout.count():
        widget = layout.takeAt(0)
        if widget:
            widget.widget().deleteLater()
class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.history = []  # List to store navigation history
        self.current_index = -1  # Index of the currently displayed page in the history
        self.baseLayout = QVBoxLayout()
        self.http_status_codes = http_status_codes
        
        self.init_ui()

    def init_ui(self):
        self.loadSettings()
        self.setGeometry(100, 100, 800, 600)

        
        self.toolbar = QToolBar()
        self.bookmarks = QToolBar()
        
        self.baseLayout.addWidget(self.toolbar)
        if self.settings["init"]["bookmarksbar"]:
            self.baseLayout.addWidget(self.bookmarks)

        address_bar_container = QWidget()
        address_bar_layout = QHBoxLayout()

        self.icon = QIcon("../img/browser.svg")
        self.setWindowIcon(self.icon)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL and press Enter")
        self.url_input.returnPressed.connect(self.load_url)
        address_bar_layout.addWidget(self.url_input)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.load_url)
        address_bar_layout.addWidget(self.go_button)

        address_bar_container.setLayout(address_bar_layout)
        self.baseLayout.addWidget(address_bar_container)

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.anchorClicked.connect(self.handle_link_click)
        self.baseLayout.addWidget(self.text_browser)


        container = QWidget()
        container.setLayout(self.baseLayout)
        self.setCentralWidget(container)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.browser_back)
        self.toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.browser_forward)
        self.toolbar.addAction(forward_action)

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.browser_refresh)
        self.toolbar.addAction(refresh_action)
        
        bookmark_action = QAction("Bookmark", self)
        bookmark_action.triggered.connect(self.bookmark_page)
        # self.toolbar.addAction(bookmark_action)

        self.url_input.setText("about:home")
        self.load_url()

        self.text_browser.viewport().installEventFilter(self)
        self.text_browser.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.LinksAccessibleByKeyboard)
        
        
        b = self.load_bookmarks()
        for item in b:
            action = QAction(item, self)
            funct = lambda _, bookmark=b[item]: self.loadPage(bookmark)
            action.triggered.connect(funct)
            self.bookmarks.addAction(action)
    def reload(self):
        clearLayout(self.baseLayout)
        self.init_ui()
    def load_bookmarks(self):
        return self.settings["bookmarks"]
    def bookmark_page(self):
        url = self.url_input.text()
        b = self.load_bookmarks()
        b[url] = url
        self.save_bookmarks(b)
        self.reload()
    def save_bookmarks(self, bookmarks):
        self.settings["bookmarks"] = bookmarks
        self.saveSettings()
    def loadPage(self, url):
        self.url_input.setText(url)
        self.load_url()
    def loadSettings(self):
        Default = {
            "init": {
                "useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "bookmarksbar":True,
                },
            "bookmarks":{
                "Home":"about:home",
                "info.cern.ch":"info.cern.ch",
                },
            }
        try:
            with open("config/system/webbrowser.toml") as f:
                self.settings = toml.load(f)
        except:
            print(traceback.format_exc())
            self.settings = Default
        self.saveSettings()
    def saveSettings(self):
        with open("config/system/webbrowser.toml","w") as f:
            toml.dump(self.settings,f)
    def generate_error_page(self, status_code, exception_message=None):
        error_message = self.http_status_codes.get(status_code, "")
        error_page = f"""
        <html>
        <body>
            {f"<h1>HTTP Error {status_code}</h1>" if status_code else "<h1>Unknown Error</h1>"}
            <p>{error_message}</p>
            {f"<p>{exception_message}</p>" if exception_message else ""}
        </body>
        </html>
        """
        return error_page
    def load_url(self):
        url = self.url_input.text()
        self.setWindowTitle("(Loading)")
        if not url.startswith("http"):
            url = "http://" + url
        if url.startswith("http://about:"):
            page = "../pages/{}.md".format(url[13:])
            if not os.path.isfile(page):
                page = "../pages/invalid.md"
            with open(page) as f:
                content = markdown.markdown(f.read())
            title = self.extract_page_title(content)
            self.text_browser.setHtml(content)
            self.setWindowTitle(title if title else "Internal Page")
        else:
            try:
                headers = {
                    'User-Agent': self.settings["init"]["useragent"]
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    content = response.text
                    title = self.extract_page_title(content)
                    content = self.convert_relative_links(content, url)

                    self.text_browser.setHtml(content)

                    if title:
                        self.setWindowTitle(title)
                    else:
                        self.setWindowTitle(url)
                    self.add_to_history(url)
                else:
                    error_html = self.generate_error_page(response.status_code)
                    self.text_browser.setHtml(error_html)
                    self.setWindowTitle("Unknown HTTP Error".format(response.status_code))
            except requests.exceptions.RequestException as e:
                error_html = self.generate_error_page(0, str(e))
                self.text_browser.setHtml(error_html)
                self.setWindowTitle("HTTP Error 0")

    def extract_page_title(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text
        else:
            return None

    def convert_relative_links(self, html_content, base_url):
        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup.find_all(['a', 'link', 'script'], href=True):
            tag['href'] = urljoin(base_url, tag['href'])
        for tag in soup.find_all(['link', 'script'], src=True):
            tag['src'] = urljoin(base_url, tag['src'])
        for img_tag in soup.find_all('img', src=True):
            img_url = urljoin(base_url, img_tag['src'])
            img_tag['src'] = img_url
            img_tag['style'] = "max-width: 100%;"
            if not img_url.startswith("http"):
                img_url = urljoin(base_url, img_url)
                img_tag['src'] = img_url
        return str(soup)

    def handle_link_click(self, url):
        self.url_input.setText(url.toString())
        self.load_url()

    def apply_hover_effect(self, event):
        text = self.text_browser.toPlainText()
        if event.type() == QEvent.HoverMove:
            hovered_link = self.text_browser.anchorAt(event.pos())
            if hovered_link:
                text = text.replace(f'<a href="{hovered_link}">', f'<a href="{hovered_link}" style="color: blue; text-decoration: underline;">')
        self.text_browser.setPlainText(text)

    def eventFilter(self, source, event):
        if source is self.text_browser.viewport():
            if event.type() in (QEvent.HoverEnter, QEvent.HoverLeave, QEvent.HoverMove):
                self.apply_hover_effect(event)
        return super().eventFilter(source, event)

    def add_to_history(self, url):
        self.history = self.history[:self.current_index + 1]
        self.history.append(url)
        self.current_index = len(self.history) - 1

    def browser_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.url_input.setText(self.history[self.current_index])
            self.load_url()

    def browser_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.url_input.setText(self.history[self.current_index])
            self.load_url()

    def browser_refresh(self):
        self.load_url()

def main():
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())



application = WebBrowser()
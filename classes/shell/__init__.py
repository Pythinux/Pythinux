from PyQt5.QtWidgets import *
import pythinux
import sys
class Application:
    def __init__(self, title, width, height):
        self.width = width
        self.height = height
        self.title = title

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def set_content_widget(self, widget):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(widget)
        self.setCentralWidget(central_widget)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == 1:  # Left mouse button pressed
            self.move(event.globalPos() - self.offset)

class WindowManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.windows = []

    def create_base_window(self, title, width, height):
        application = Application(title, width, height)
        base_window = BaseWindow()
        base_window.setWindowTitle(application.title)
        base_window.resize(application.width, application.height)
        self.windows.append(base_window)
        return base_window

    def add_window(self, base_window, application):
        sub_window = QMainWindow(base_window)
        sub_window.setWindowTitle(application.title)
        sub_window.resize(application.width, application.height)
        self.windows.append(sub_window)
        sub_window.show()

    def on_base_window_closed(self):
        self.app.quit()

    def start(self):
        for base_window in self.windows:
            base_window.destroyed.connect(self.on_base_window_closed)
            base_window.show()

        sys.exit(self.app.exec_())
def startShell():
    manager = WindowManager()
    base = manager.create_base_window("Pythinux {} (Unstable Pre-Release)".format(".".join([str(x) for x in pythinux.version])), 1600, 900)
    layout = QGridLayout()
    msg = [
        "Welcome to Pythinux."
    ]
    msg = "\n".join(msg)
    label = QLabel(msg)
    layout.addWidget(label,0,0)
    manager.start()
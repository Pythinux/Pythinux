from PyQt5.QtWidgets import *
import os
import time

x = os.getcwd()
import pythinux
os.chdir(x)

import sys
import subprocess
import pickle
from PyQt5.QtCore import Qt
import base64
import toml
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
import markdown
def getIconList(currentUser):
    l = [
            {
                "name":"Terminal Emulator",
                "link":"terminal",
                "icon":"terminal",
                "elevate":False,
            },
            {
                "name":"Help Topics",
                "link":"guihelp",
                "icon":"guihelp",
                "elevate":False,
            },
            {
                "name":"Settings",
                "link":"settings",
                "icon":"settings",
                "elevate":True,
            },
            {
                "name":"Software Centre",
                "link":"softwarecenter",
                "icon":"softwarecenter",
                "elevate":True,
            },
            {
                "name":"Binary Tally",
                "link":"binc",
                "icon":"binary-tally",
                "elevate":False,
            },
            {
                "name":"Web Browser",
                "link":"webbrowser",
                "icon":"browser",
                "elevate":False,
            },
            {
                "name":"Blackjack",
                "link":"blackjack",
                "icon":"crown",
                "elevate":False,
            },
            {
                "name":"Calculator",
                "link":"calculator",
                "icon":"calculator",
                "elevate":False,
            },
            {
                "name":"Currencies",
                "link":"currencies",
                "icon":"coinbag",
                "elevate":False,
            },
        ]
    z = []
    for item in l:
        if item["link"] in pythinux.list_loadable_programs(currentUser):
            z.append(item)
    files = [x for x in os.listdir("icon") if x.endswith(".entry")]
    for f in files:
        with open("icon/{}".format(f)) as f:
            x = toml.loads(f.read())
            try:
                z = x["Desktop Entry"]
                _, _, _ = z["name"], z["link"], z["icon"]
                l.append(z)
            except:
                pass
    return sorted(l, key=lambda x: x['name'])
class WindowManager:
    def __init__(self, user):
        self.windows = []
        self.app = QApplication([])
        mode = "dark"
        color = "#D84727"
        qdarktheme.setup_theme(
            custom_colors={
                "[dark]": {
                    "primary": color,
                }
            }
        )
        self.user = user

    def add_window(self, window):
        if isinstance(window, QMainWindow):
            self.windows.append(window)
            window.show()
        else:
            raise ValueError("Invalid window type. Only QMainWindow is supported.")

    def remove_window(self, window):
        if window in self.windows:
            self.windows.remove(window)
            window.close()
        else:
            raise ValueError("Window not found in the window manager.")

    def run(self):
        self.app.exec_()
class CommandThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        process = subprocess.Popen(
            self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        while process.poll() is None:
            output = process.stdout.readline().strip()
            if output:
                self.output_signal.emit(output)
        self.output_signal.emit("")  # Signal completion

class TerminalApp(QMainWindow):
    def __init__(self, currentUser):
        super().__init__()
        self.init_ui()
        self.currentUser = currentUser
        self.icon = QIcon("../img/terminal.svg")
        self.setWindowIcon(self.icon)

    def init_ui(self):
        self.setWindowTitle("Terminal Emulator")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.cursor = self.output_area.textCursor()
        layout.addWidget(self.output_area)

        self.input_field = QLineEdit(self)
        self.input_field.returnPressed.connect(self.process_command)
        layout.addWidget(self.input_field)

        self.setCentralWidget(central_widget)
        self.thread = None  # To keep track of the running thread

    def process_command(self):
        if self.thread is not None and self.thread.isRunning():
            return  # Don't start a new command while one is already running

        user_input = self.input_field.text()
        self.input_field.clear()
        self.cursor.movePosition(self.cursor.End)
        self.output_area.setTextCursor(self.cursor)
        self.output_area.insertPlainText(f"{self.currentUser.group.name}@{self.currentUser.username} ${user_input}\n")
        
        if user_input.lower() in ['clear', 'cls']:
            # Clear the terminal output
            self.output_area.clear()
        elif user_input.lower() in ["exit", "quit"]:
            self.close()
        else:
            u = pythinux.serialiseToDict(self.currentUser)
            u = pickle.dumps(u)
            u = base64.b64encode(u).decode("ascii")
            cmd = [
                "python", "-c",
                f"import os; os.chdir('..'); import pythinux; x = pythinux.main('{u}','{user_input}');print(x if x else '')"
            ]
            
            self.thread = CommandThread(cmd)
            self.thread.output_signal.connect(self.update_output)
            self.thread.finished.connect(self.command_finished)
            self.input_field.setEnabled(False)  # Disable input while command is running
            self.thread.start()

    def command_finished(self):
        self.input_field.setEnabled(True)  # Enable input after the command finishes
        self.input_field.setFocus()  # Move focus back to the input field

    def update_output(self, output):
        self.cursor.movePosition(self.cursor.End)
        self.output_area.setTextCursor(self.cursor)
        self.output_area.insertPlainText(output + "\n")

    def enable_input(self):
        self.input_field.setEnabled(True)
class OtherCommandThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        import subprocess
        result = subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout + result.stderr
        self.output_signal.emit(output)

class ShowTerminal(QDialog):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.thread = None  # Initialize thread to None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Show Terminal")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    def start_execution(self):
        if self.thread is not None and self.thread.isRunning():
            return  # Don't start a new thread if one is already running

        cmd = [
            "python", "-c",
            f"import os; os.chdir('..'); import pythinux; x = pythinux.main('','{self.command}');print(x if x else '')"
        ]
        self.thread = OtherCommandThread(cmd)
        self.thread.output_signal.connect(self.update_output)
        self.thread.finished.connect(self.command_finished)
        self.thread.start()

    def command_finished(self):
        self.thread.quit()  # Quit the thread
        self.thread.wait()  # Wait for the thread to finish
        self.accept()  # Close the dialog

    def update_output(self, output):
        cursor = self.output_area.textCursor()
        cursor.movePosition(cursor.End)
        self.output_area.setTextCursor(cursor)
        self.output_area.insertPlainText(output + "\n")
   
def loadProgram(item, currentUser, manager, needAdmin):
    try:
        i = pythinux.load_program(item, currentUser)
        i = i.application
        manager.add_window(i)
    except:
        print(traceback.format_exc())
class HelpTopicsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Help Topics')
        self.setGeometry(100, 100, 800, 600)
        self.icon = QIcon("../img/guihelp.svg")
        self.setWindowIcon(self.icon)

        # Create a QFileSystemModel to populate the tree view
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Set an initial path
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        # Specify the path to the help topics folder
        help_topics_folder = '../helptopics'
        root_index = self.model.index(help_topics_folder)
        if root_index.isValid():
            self.model.setRootPath(self.model.filePath(root_index))
            self.tree_view = QTreeView(self)
            self.tree_view.setModel(self.model)
            self.tree_view.setRootIndex(root_index)

            # Hide the unnecessary size, type, and date fields from the header
            header = self.tree_view.header()
            header.setSectionHidden(1, True)  # Size column
            header.setSectionHidden(2, True)  # Type column
            header.setSectionHidden(3, True)  # Date column

            # Create a QTextBrowser widget to display the help topics content
            self.text_browser = QTextBrowser()

            # Create a layout to arrange the tree view and text browser vertically
            layout = QHBoxLayout()
            layout.addWidget(self.tree_view)
            layout.addWidget(self.text_browser)

            # Create a central widget and set the layout
            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            # Connect the item selection signal to show_help_content method
            self.tree_view.selectionModel().selectionChanged.connect(self.show_help_content)

            # Set custom icons for directories and files
            self.tree_view.setItemDelegate(MyItemDelegate())

        else:
            print(f"Invalid root index: {help_topics_folder}")

    def show_help_content(self, selected, deselected):
        # Get the path of the selected item
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            path = self.model.filePath(index)

            # Check if the selected item is a file
            if self.model.isDir(index):
                # Clear the QTextBrowser if a directory is selected
                self.text_browser.setPlainText('')
            else:
                # Read the content of the selected help topic file and display it in the QTextBrowser
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    html_content = markdown.markdown(content)
                    self.text_browser.setHtml(html_content)


class MyItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.model().isDir(index):
            option.icon = QIcon('../img/folder.svg')  # Replace with your custom folder icon path
        else:
            option.icon = QIcon('../img/file.svg')  # Replace with your custom file icon path
def check_button_exists(layout):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QPushButton) and widget.text() == "Exit":
            return True
    return False
class ProgramLoader(QMainWindow):
    def __init__(self, user, manager):
        super().__init__()
        self.user=user
        self.manager = manager
        self.icon = QIcon("../img/progmgr.svg")
        self.setWindowIcon(self.icon)
        self.init_ui()
        self.load_icons()
        
    def init_ui(self):
        self.setWindowTitle("Program Manager")
        
        self.menubar = self.menuBar()
        self.fileMenu = QMenu("File")
        self.menubar.addMenu(self.fileMenu)
        self.refresh_action = QAction("Refresh", self)
        self.refresh_action.setShortcut("F5")
        self.refresh_action.triggered.connect(self.refresh)
        self.fileMenu.addAction(self.refresh_action)
        
        self.central_widget = QWidget(self)
        self.frame = QFrame()
        self.baseLayout = QVBoxLayout(self.central_widget)
        self.baseLayout.addWidget(self.frame)
        self.layout = QGridLayout(self.frame)

        self.setCentralWidget(self.central_widget)
    def load_icons(self):
        icons = []
        for item in getIconList(self.user):
            if item["icon"]:
                if isinstance(item["icon"],str):
                    icon = QIcon("../img/{}.svg".format(item["icon"]))
                else:
                    icon = QIcon("icon/{}.svg".format(item["name"]))
            else:
                icon = QIcon("../img/default.svg")
            action = QAction("Load", self)
            action.triggered.connect(lambda _, link=item["link"]: loadProgram(link, self.user, self.manager, item["elevate"]))
            icons.append((icon, action, item))

        x, y = 0, 0
        for icon, action, item in icons:
            button = QToolButton()
            button.setIcon(icon)
            button.setIconSize(QSize(64, 64))
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setText(item["name"])
            button.clicked.connect(action.triggered)
            self.layout.addWidget(button, x, y)
            y += 1
            if y >= 5:
                x += 1
                y = 0
        if not check_button_exists(self.baseLayout):
            self.button = QPushButton("Exit")
            self.button.clicked.connect(sys.exit)
            self.baseLayout.addWidget(self.button)
    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                clear_layout(item.layout())
    def refresh(self):
        self.clear_layout()
        print("Did Refresh")
        self.load_icons()
    def closeEvent(self, event):
        sys.exit()
class Application:
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
def startShell(currentUser):
    manager = WindowManager(currentUser)
    
    # terminal = TerminalApp(currentUser)
    program_loader = ProgramLoader(currentUser, manager)
    
    # manager.add_window(terminal)
    manager.add_window(program_loader)
    
    manager.run()
if __name__ == "__main__":
    # Perform necessary imports here (e.g., pythinux)
    startShell(currentUser)  # Call the startShell function
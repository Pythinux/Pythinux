x = os.getcwd()
import pythinux
os.chdir(x)

pkm = pythinux.load_library("pkm",currentUser)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Manage(QDialog):
    def __init__(self):
        super().__init__()
        self.base = QVBoxLayout(self)
        self.setLayout(self.base)
        self.didInit = False
        
        self.init_ui()
        self.init_list()
        self.init_config()
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.frame=QFrame()
        self.frame.setLayout(self.layout)
        self.base.addWidget(self.frame)
        self.splitter = QSplitter(Qt.Horizontal)  # Create a horizontal splitter

        self.listBase = QGroupBox("Program List")
        self.listLayout = QVBoxLayout(self.listBase)

        self.configBase = QGroupBox("Configuration")

        self.splitter.addWidget(self.listBase)
        self.splitter.addWidget(self.configBase)

        self.splitter.setSizes([1, 1])  # Equal sizes for both widgets
        self.layout.addWidget(self.splitter)
        
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.clicked.connect(self.refresh)
        self.layout.addWidget(self.refreshButton)
        
        self.didInit = True
    def remove(self):
        pkg = self.combo.currentText()
        deps = pkm.findDeps(pkg)
        if deps:
            msg = "This package cannot be removed due to certain programs requiring it.\n"
            msg += "Remove those programs first.\n"
            msg += "The programs are:\n{}".format("; ".join(deps))
            m = MessageBox("Error",msg)
        else:
            cmd = "pkm remove '{}'".format(pkg)
            main(currentUser, cmd)
        self.refresh()
    def view_info(self):
        pkginf = pkm.loadPackageInfs()
        pkgName = self.combo.currentText()
        pkgDeps = pkm.findDeps(pkgName)
        pkgDeps = ";".join(pkgDeps) if pkgDeps else "Nothing"
        pkg = pkginf[pkgName]
        
        msg = "Name: {}\n".format(pkg["humanName"])
        msg += "Author: {}\n".format(pkg["author"])
        msg += "Version: {}\n".format(".".join(pkg["version"]))
        msg += "Release Date: {}\n".format(pkg["releaseDate"])
        msg += "Dependencies: {}\n".format("; ".join(pkg["deps"]) if pkg["deps"] else "None")
        msg += "Required By: {}\n".format(pkgDeps)
        msg += "Package Type: {}\n".format('Binary' if bool(pkg["binary"]) else 'Library')
        
        m = MessageBox("Package Info",msg)
    def configOptions(self):
        if self.checkClear.isChecked():
            cmd = "pkm clear"
            main(currentUser,cmd)
        self.refresh()
    def init_list(self):
        self.combo = QComboBox()
        
        for item in pkm.list_app():
            self.combo.addItem(item)
        enabled = bool(pkm.list_app())
        self.selectLabel = QLabel("Select Program")
        self.infoButton = QPushButton("View Program Info")
        self.removeButton = QPushButton("Remove Program")
        self.removeButton.clicked.connect(self.remove)
        self.infoButton.clicked.connect(self.view_info)
        self.infoButton.setEnabled(enabled)
        self.removeButton.setEnabled(enabled)
        
        self.listLayout.addWidget(self.selectLabel)
        self.listLayout.addWidget(self.combo)
        self.listLayout.addWidget(self.infoButton)
        self.listLayout.addWidget(self.removeButton)
        
        self.listLayout.addStretch()
    def init_config(self):
        self.configLayout = QVBoxLayout()
        self.configBase.setLayout(self.configLayout)
        
        self.checkClear = QCheckBox("Remove all programs")
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.clicked.connect(self.configOptions)
        
        self.configLayout.addWidget(self.checkClear)
        self.configLayout.addWidget(self.confirmButton)
        self.configLayout.addStretch()
    def clear_layout(self):
        while self.base.count():
            item = self.base.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    def refresh(self):
        self.clear_layout()
        self.init_ui()
        self.init_list()
        self.init_config()
class UpdatingScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        loading = QLabel("Updates are being installed.\nThis may take a while.")
        layout.addWidget(loading, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)
        self.centerOnScreen()

    def centerOnScreen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        loading = QLabel("Loading Software Centre...")
        loading.setStyleSheet('background-color: #000000; color: white;')
        layout.addWidget(loading, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

        pixmap = QPixmap("../img/splash/softwarecenter.png")
        self.setPixmap(pixmap)

        self.centerOnScreen()

    def centerOnScreen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

class Update(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_upgrades()
        self.init_ui()

    def init_ui(self):
        self.refreshButton = QPushButton("Reload")
        self.refreshButton.clicked.connect(self.refresh)
        self.loadLabel = QLabel()
        if self.upgrades:
            if len(self.upgrades) == 1:
                label = QLabel("1 update is ready to be installed.")
            else:
                label = QLabel("{} updates are ready to be installed.".format(len(self.upgrades)))
            button = QPushButton("Install Updates")
            button.clicked.connect(self.upgrade)
            self.layout.addWidget(label)
            self.layout.addWidget(button)
        else:
            label = QLabel("No updates to install.")
            self.layout.addWidget(label)
        self.layout.addStretch()
        self.layout.addWidget(self.refreshButton)
    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    def upgrade(self):
        cmd = "pkm upgrade"
        s = UpdatingScreen()
        s.show()
        main(currentUser,"pkm upgrade")
        s.close()
        self.refresh()
    def init_upgrades(self):
        apps = pkm.list_app()
        infs = pkm.loadPackageInfs()
        dbs = pkm.give_dbs(True,True)
        self.upgrades = []
        for item in apps:
            if dbs[item]["version"] > infs[item]["version"]:
                self.upgrades.append(item)

        # Process pending events to ensure UI updates before continuing
        QCoreApplication.processEvents()

    def refresh(self):
        self.clear_layout()
        self.init_upgrades()
        self.init_ui()
class Databases(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.init_ui()
        
    def init_ui(self):
        self.splitter = QSplitter(Qt.Horizontal)
        
        self.dbListBase = QGroupBox("Databases")
        self.configBatch = QVBoxLayout()
        self.configBase = QGroupBox("Create Database")
        
        self.dbList = QVBoxLayout(self.dbListBase)
        self.config = QVBoxLayout(self.configBase)
        
        self.splitter.addWidget(self.dbListBase)
        self.splitter.addWidget(self.configBase)
        
        self.layout.addWidget(self.splitter)
        
        self.frame = QFrame()
        self.configBatch = QVBoxLayout()
        self.frame.setLayout(self.configBatch)
        
        for item in pkm.update_db():
            box = QGroupBox(item)
            lay = QVBoxLayout(box)
            button = QPushButton("Remove")
            button.clicked.connect(lambda _, item=item: self.remove(item))
            lay.addWidget(button)
            self.dbList.addWidget(box)
        self.dbList.addStretch()
        
        self.nameLabel = QLabel("Name of Database:")
        self.nameInput = QLineEdit()
        self.urlLabel = QLabel("URL:")
        self.urlInput = QLineEdit()
        self.button = QPushButton("Add Database")
        self.button.clicked.connect(self.add_database)
        
        self.config.addWidget(self.nameLabel)
        self.config.addWidget(self.nameInput)
        self.config.addWidget(self.urlLabel)
        self.config.addWidget(self.urlInput)
        self.config.addWidget(self.button)
        self.config.addStretch()
        
        self.configBatch.addStretch()
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.clicked.connect(self.refresh)
        self.configBatch.addWidget(self.refreshButton)
    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def remove(self, item):
        db = pkm.update_db()
        db.pop(item)
        pkm.save_db(db)
        self.refresh()
        
    def add_database(self):
        name, url = self.nameInput.text(), self.urlInput.text()
        if name and url:
            db = pkm.update_db()
            db[name] = url
            pkm.save_db(db)
        self.refresh()
        
    def refresh(self):
        self.clear_layout()
        self.init_ui()

class Tab:
    def __init__(self, name, tab):
        self.name = name
        self.tab = tab

class SoftwareCenter(QMainWindow):
    def __init__(self, currentUser):
        super().__init__()
        self.icon = QIcon("../img/softwarecenter.svg")
        self.setWindowIcon(self.icon)
        self.user = currentUser
        self.setWindowTitle("Software Centre")
        self.setFixedSize(800, 600)
        self.setGeometry(100, 100, 800, 600)
        self.init_tabs()
        self.init_ui()

    def init_tabs(self):
        self.tab_items = [
            Tab("Updates",Update),
            Tab("Manage",Manage),
            Tab("Databases",Databases),
        ]

    def init_ui(self):
        self.central = QWidget(self)
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        for item in self.tab_items:
            tabClass = item.tab()
            self.tabs.addTab(tabClass, item.name)    
splash = SplashScreen()
splash.show()
application = SoftwareCenter(currentUser)
splash.finish(application)
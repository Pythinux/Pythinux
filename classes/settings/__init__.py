#!/usr/bin/python
import os
import sys
x = os.getcwd()
import pythinux
os.chdir(x)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarktheme
import pickle
import copy

class DataBundle:
    def add(self,name,value):
        setattr(self,name,value)
class Preferences(DataBundle):
    def __init__(self):
        super().__init__()
        self.add("accentColour","Default")
def loadPreferences():
    try:
        with open("config/system/shell.cfg","rb") as f:
            return pickle.load(f)
    except:
        p = Preferences()
        return savePreferences(p)
def savePreferences(p):
    if isinstance(p,Preferences):
        with open("config/system/shell.cfg","wb") as f:
            f.write(p)
    return p
def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()

        if widget:
            widget.setParent(None)  # Remove widget from the layout and delete it
        else:
            clearLayout(item.layout())  # Recursively clear sub-layouts

        del item  # Delete the layout item to avoid memory leaks
class GroupSettings(QWidget):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()

        self.setLayout(self.layout)
        
        self.load_groups()
        self.load_settings()
    def load_groups(self):
        self.groupListBase = QGroupBox("Groups")
        self.groupConfigBase = QGroupBox("Configure")

        self.layout.addWidget(self.groupListBase)
        self.layout.addWidget(self.groupConfigBase)

        self.groupList = QVBoxLayout(self.groupListBase)
        self.groupConfig = QVBoxLayout(self.groupConfigBase)

        i = 1
        for item in pythinux.loadGroupList().list():
            group = QGroupBox("Group: {}".format(item.name))
            lay = QVBoxLayout(group)
            if item.builtin:
                view_button = QPushButton("View Permissions")
            else:
                view_button = QPushButton("Edit Permissions")
            data = pythinux.DataBundle()
            data.add("name", item.name)
            data.add("edit", not item.builtin)

            # Fix lambda expressions to capture data correctly
            view_button.clicked.connect(lambda _, data=data: self.edit_group(data))
            remove_button = QPushButton("Remove Group")
            remove_button.clicked.connect(lambda _, name=item.name: self.remove_group(name))

            if item.locked:
                remove_button.setEnabled(False)

            lay.addWidget(view_button)
            lay.addWidget(remove_button)
            self.groupList.addWidget(group)
            i += 1
        self.groupList.addStretch()        
    def refresh(self):
        clearLayout(self.layout)
        self.load_groups()
        self.load_settings()
    def load_settings(self):
        self.newGroupBase = QGroupBox("Create Group")
        
        self.groupNameLabel = QLabel("Group name:")
        self.groupName = QLineEdit()
        self.canApp = QCheckBox("Run Installed Apps")
        self.canAppHigh = QCheckBox("Run Elevated Installed Apps")
        self.canSys = QCheckBox("Run Elevated System Programs")
        self.canSysHigh = QCheckBox("Run God-Level System Programs")
        self.canSudo = QCheckBox("Use `sudo`")
        self.newButton = QPushButton("Create Group")
        self.newButton.clicked.connect(self.create_group)
        
        self.newGroup = QVBoxLayout(self.newGroupBase)
        
        self.newGroup.addWidget(self.groupNameLabel)
        self.newGroup.addWidget(self.groupName)
        self.newGroup.addWidget(self.canApp)
        self.newGroup.addWidget(self.canAppHigh)
        self.newGroup.addWidget(self.canSys)
        self.newGroup.addWidget(self.canSysHigh)
        self.newGroup.addWidget(self.canSudo)
        self.newGroup.addWidget(self.newButton)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)
        
        self.groupConfig.addWidget(self.newGroupBase)
        self.groupConfig.addStretch()
        self.groupConfig.addWidget(self.refresh_button)
    def edit_group(self, data):
        class EditGroup(QDialog):
            def __init__(self, data):
                super().__init__()
                self.canEdit = data.edit
                self.group = pythinux.loadGroupList().byName(data.name)
                self.init_ui()
            def init_ui(self):
                self.setWindowTitle("Edit Group Permissions For {}".format(self.group.name))
                self.setGeometry(200, 200, 300, 200)
                self.layout = QVBoxLayout(self)
                
                self.canApp = QCheckBox("Run Installed Apps")
                self.canAppHigh = QCheckBox("Run Elevated Installed Apps")
                self.canSys = QCheckBox("Run Elevated System Programs")
                self.canSysHigh = QCheckBox("Run God-Level System Programs")
                self.canSudo = QCheckBox("Use `sudo`")
                
                self.canApp.setChecked(self.group.canApp)
                self.canAppHigh.setChecked(self.group.canAppHigh)
                self.canSys.setChecked(self.group.canSys)
                self.canSysHigh.setChecked(self.group.canSysHigh)
                self.canSudo.setChecked(self.group.canSudo)
                
                self.canApp.setEnabled(self.canEdit)
                self.canAppHigh.setEnabled(self.canEdit)
                self.canSys.setEnabled(self.canEdit)
                self.canSysHigh.setEnabled(self.canEdit)
                self.canSudo.setEnabled(self.canEdit)
                
                self.button = QPushButton("Done")
                self.button.clicked.connect(self.close)
                
                self.layout.addWidget(self.canApp)
                self.layout.addWidget(self.canAppHigh)
                self.layout.addWidget(self.canSys)
                self.layout.addWidget(self.canSysHigh)
                self.layout.addWidget(self.canSudo)
                self.layout.addWidget(self.button)
                
        root = EditGroup(data)
        root.show()
        root.exec_()
        
        root.group.canApp = root.canApp.isChecked()
        root.group.canAppHigh = root.canAppHigh.isChecked()
        root.group.canSys = root.canSys.isChecked()
        root.group.canSysHigh = root.canSysHigh.isChecked()
        root.group.canSudo = root.canSudo.isChecked()
        
        groupList = pythinux.loadGroupList()
        groupList.add(root.group)
        pythinux.saveGroupList(groupList)
        
        
    def create_group(self):
        if self.groupName.text():
            cmd = "group add '{}' {} {} {} {} {}".format(
                self.groupName.text(),
                int(self.canApp.isChecked()),
                int(self.canAppHigh.isChecked()),
                int(self.canSys.isChecked()),
                int(self.canSysHigh.isChecked()),
                int(self.canSudo.isChecked()),
                )
            pythinux.main(self.base.currentUser,cmd)
        else:
            print("A group name is requried.")
        self.refresh()
    def remove_group(self, name):
        pythinux.main(self.base.currentUser,"group remove '{}'".format(name))
        self.refresh()
        
class UserSettings(QWidget):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.init_ui()
    def remove_user(self, user):
        cmd = "user remove '{}'".format(user.username)
        pythinux.main(self.base.currentUser,cmd)
        self.refresh()
    def init_ui(self):
        helpTopicsAction = QAction("Refresh",self)
        helpTopicsAction.triggered.connect(self.refresh)
        helpTopicsAction.setShortcut("F5")
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.init_users()
        self.init_settings()
    def create_user(self):
        u, p, g  = self.username_input.text(), self.password_input.text(), self.groupList.currentText()
        if u and p:
            cmd = "user add '{}' '{}' '{}'".format(u,p,g)
            pythinux.main(self.base.currentUser,cmd)
        self.refresh()
    def init_users(self):
        self.groupbox = QGroupBox("Users")
        self.userListBase = QVBoxLayout()
        self.frame = QFrame()
        self.userList = QVBoxLayout()
        self.groupbox.setLayout(self.userListBase)
        self.frame.setLayout(self.userList)
        self.userListBase.addWidget(self.frame)
        self.layout.addWidget(self.groupbox)
        i = 1
        for item in pythinux.loadUserList().list():
            box = QGroupBox("User #{}".format(i))
            lay = QVBoxLayout()
            box.setLayout(lay)
            msg = [
                "Username: {}".format(item.username),
                "Group: {}".format(item.group.name),
                ]
            msg = "\n".join(msg)
            label = QLabel(msg)
            label.setAlignment(Qt.AlignCenter)
            bt = QPushButton("Remove User")
            bt.clicked.connect(lambda _, user=item: self.remove_user(user))
            if not self.base.currentUser.admin():
                bt.setEnabled(False)
            lay.addWidget(label)
            lay.addWidget(bt)
            self.scrollbar = QScrollBar(Qt.Horizontal)
            self.userList.addWidget(box)
            i += 1
        self.userList.addStretch()
    def refresh(self):
        clearLayout(self.layout)
        self.init_users()
        self.init_settings()
    def autologin(self):
        cmd = "autologin '{}'".format(self.AutoLoginBox.currentText() if self.AutoLoginBox.currentText() else "--reset")
        pythinux.main(self.base.currentUser,cmd)
        self.refresh()
    def init_settings(self):
        self.generalSettings = QGroupBox("Configure Users")
        self.userSettings = QVBoxLayout()
        
        self.generalSettings.setLayout(self.userSettings)
        self.layout.addWidget(self.generalSettings)
        self.layout.setStretchFactor(self.groupbox, 1)
        self.layout.setStretchFactor(self.generalSettings, 1)
        
        self.createUserBase = QGroupBox("Create User")
        self.createUser = QVBoxLayout()
        self.createUserBase.setLayout(self.createUser)
        
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.groupList = QComboBox()
        for item in pythinux.loadGroupList().list():
            self.groupList.addItem(item.name)
        self.groupLabel = QLabel("Select the user's group:")
        
        self.createUserButton = QPushButton("Create User")
        self.createUserButton.clicked.connect(self.create_user)
        if not self.base.currentUser.admin():
            self.createUserButton.setEnabled(False)
        
        self.createUser.addWidget(self.username_label)
        self.createUser.addWidget(self.username_input)
        self.createUser.addWidget(self.password_label)
        self.createUser.addWidget(self.password_input)
        self.createUser.addWidget(self.groupLabel)
        self.createUser.addWidget(self.groupList)
        self.createUser.addWidget(self.createUserButton)
        
        
        self.userSettings.addWidget(self.createUserBase)
        
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.clicked.connect(self.refresh)
        
        
        self.autoLoginMenu = QGroupBox("Automatic Login")
        self.autoLoginFrame = QVBoxLayout()
        self.autoLoginMenu.setLayout(self.autoLoginFrame)
        self.AutoLoginBox = QComboBox()
        self.AutoLoginBox.addItem("")
        l = [x.username for x in pythinux.loadUserList().list()]
        for i in l:
            self.AutoLoginBox.addItem(i)
        u = pythinux.loadAL()
        self.AutoLoginBox.setCurrentText(u if u else "")
        
        self.autoLoginButton = QPushButton("Set User As Default")
        self.autoLoginButton.clicked.connect(self.autologin)
        if not self.base.currentUser.admin():
            self.autoLoginButton.setEnabled(False)
        
        self.autoLoginFrame.addWidget(self.AutoLoginBox)
        self.autoLoginFrame.addWidget(self.autoLoginButton)
        
        self.userSettings.addWidget(self.autoLoginMenu)
        self.userSettings.addStretch()
        self.userSettings.addWidget(self.refreshButton)
        
    
class Setting:
    def __init__(self, title, icon_name=None, className=None):
        self.title = title
        self.icon_name = icon_name
        self.className = className


class SettingsApp(QMainWindow):
    def __init__(self,currentUser):
        super().__init__()
        self.currentUser = currentUser
        self.init_settings()
        self.init_ui()
    def init_settings(self):
        self.settings = [
                Setting("Users","user",UserSettings),
                Setting("Groups","group",GroupSettings),
            ]
    def init_ui(self):
        self.menubar = self.menuBar()
        self.fileMenu = QMenu("File")
        self.menubar.addMenu(self.fileMenu)
        self.refreshAction = QAction("Refresh")
        self.refreshAction.triggered.connect(self.refresh)
        self.refreshAction.setShortcut("F5")
        self.fileMenu.addAction(self.refreshAction)
        
        self.layout = QVBoxLayout()
        self.setWindowTitle("Pythinux Settings")
        self.setGeometry(100, 100, 800, 600)
        self.icon = QIcon("../img/settings.svg")
        self.setWindowIcon(self.icon)
        
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.load_icons()
    def refresh(self):
        clearLayout(self.layout)
        self.init_ui()
    def load_icons(self):
        x,y = 0,0
        for item in self.settings:
            if item.icon_name:
                icon = QIcon("../img/settings/{}.svg".format(item.icon_name))
            else:
                icon = QIcon("../img/settings.svg")
            if item.className:
                tabClass = item.className(self)
            else:
                tabClass = QWidget()
            self.tab_widget.addTab(tabClass, icon, item.title)
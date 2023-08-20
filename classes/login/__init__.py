import pythinux
from PyQt5.QtWidgets import *
from classes import shell
import sys
def loginScreen():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Login')
    
    username_label = QLabel('Username:')
    username_input = QLineEdit()
    
    password_label = QLabel('Password:')
    password_input = QLineEdit()
    password_input.setEchoMode(QLineEdit.Password)  # To hide the password input
    
    login_button = QPushButton('Login')
    login_button.clicked.connect(app.quit)
    
    quitButton = QPushButton('Exit')
    quitButton.clicked.connect(sys.exit)
    
    layout = QGridLayout()
    layout.addWidget(username_label,0,0)
    layout.addWidget(username_input,0,1)
    layout.addWidget(password_label,1,0)
    layout.addWidget(password_input,1,1)
    layout.addWidget(login_button,2,1)
    layout.addWidget(quitButton,2,0)
    
    window.setLayout(layout)
    window.show()
    
    # Start the event loop and wait for the application to finish (when app.quit() is called)
    app.exec_()

    # Return the username and password provided by the user
    username = username_input.text()
    password = password_input.text()
    return username, password
def unlockScreen():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Unlock Your PC')
    
    password_label = QLabel('Password:')
    password_input = QLineEdit()
    password_input.setEchoMode(QLineEdit.Password)  # To hide the password input
    
    login_button = QPushButton('Unlock PC')
    login_button.clicked.connect(app.quit)  # Close the application when login button is clicked
    
    quitButton = QPushButton('Exit')
    quitButton.clicked.connect(sys.exit)
    
    layout = QGridLayout()
    layout.addWidget(password_label,0,0)
    layout.addWidget(password_input,0,1)
    layout.addWidget(login_button,1,1)
    layout.addWidget(quitButton,1,0)
    
    window.setLayout(layout)
    window.show()
    
    # Start the event loop and wait for the application to finish (when app.quit() is called)
    app.exec_()

    # Return the username and password provided by the user
    password = password_input.text()
    return password
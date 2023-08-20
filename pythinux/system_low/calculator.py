from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import math
def roundDP(x, y):
    try:
        x = float(x)
        power = 10 ** y
        rounded = round(x * power) / power
        return rounded
    except ValueError:
        raise ValueError("Invalid input: x must be a numeric value")
from math import log10, floor
def roundSFBase(x, sig=2):
    return round(float(x), sig-int(floor(log10(abs(x))))-1)
def roundSF(self,x):
    y = float(fl.getText(self.display))
    fl.setText(self.display, roundSFBase(y,x))
def roundInt(num):
    return round(num,2)
def Sin(degrees):
    radians = math.radians(degrees)
    return math.sin(radians)

def Cos(degrees):
    radians = math.radians(degrees)
    return math.cos(radians)

def Tan(degrees):
    radians = math.radians(degrees)
    return math.tan(radians)
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Calculator")
        self.icon = QIcon("../img/calculator.svg")
        self.setWindowIcon(self.icon)
        w, h = self.width(), self.height()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.base = QVBoxLayout(self.central_widget)

        self.grid = QGridLayout()
        self.frame = QFrame()
        
        self.result = 0

        self.text = QLineEdit()
        self.base.addWidget(self.text)
        
        self.mem = "0"
        
        self.menu = self.menuBar()
        self.fileMenu = QMenu("File")
        self.editMenu = QMenu("Edit")
        self.helpMenu = QMenu("Help")
        self.menu.addMenu(self.fileMenu)
        self.menu.addMenu(self.editMenu)
        self.menu.addMenu(self.helpMenu)
        
        self.exitAction = QAction("Exit")
        self.exitAction.triggered.connect(self.close)
        self.exitAction.setShortcut(QKeySequence.Quit)
        self.fileMenu.addAction(self.exitAction)
        
        self.clearAction = QAction("Clear")
        self.clearAction.triggered.connect(self.clear)
        self.clearAction.setShortcut("Esc")
        self.editMenu.addAction(self.clearAction)
        
        self.solveAction = QAction("Solve")
        self.solveAction.triggered.connect(lambda:self.button_clicked("="))
        self.solveAction.setShortcut("Return")
        self.editMenu.addAction(self.solveAction)
        
        self.buttons = [
            ["7", "8", "9", "/", "Sin","MS"],
            ["4", "5", "6", "*", "Cos","M"],
            ["1", "2", "3", "-", "Tan","MC"],
            ["0", ".", "C", "+", "(", ")"],
            ["Rnd", "=", "Ans", "^", "Rand", "Sqrt"],
            ["!", "pi", "e", "*10^", "Int", "Flt"],
            # ["","","","","",""],
        ]
        self.blacklist = ["Rand","*10^","!","^",""]
        x, y = 0, 0
        for row in self.buttons:
            for item in row:
                b = QPushButton(item)
                b.setFixedSize(50, 40)
                function = lambda _, button=item: self.button_clicked(button)
                if item in self.blacklist:
                    b.setEnabled(False)
                b.clicked.connect(function)
                self.grid.addWidget(b, x, y)
                y += 1
            x += 1
            y = 0

        self.frame.setLayout(self.grid)
        self.base.addWidget(self.frame)

        self.setLayout(self.base)
        
        self.frame.setLayout(self.grid)
        self.base.addWidget(self.frame)
    def clear(self):
        self.text.setText("")
    def button_clicked(self, button):
        button = button.replace("^","**")
        if button == "=":
            if self.text.text():
                try:
                    result = doCalc(self.text.text())
                except Exception as e:
                    result = "Error: {}".format(e)
            else:
                result = ""
            if result:
                self.result = result
            self.text.setText(str(result))
        elif button == "MS":
            self.mem = self.text.text()
        elif button == "M":
            self.text.setText(self.mem)
        elif button == "MC":
            self.mem = "0"
        elif button == "Sin":
            try:
                t = float(self.text.text())
                t = Sin(t)
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "Cos":
            try:
                t = float(self.text.text())
                t = Cos(t)
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "Rnd":
            try:
                t = self.text.text()
                t = roundDP(t,3)
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "Int":
            try:
                t = self.text.text()
                t = int(float(t))
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "Flt":
            try:
                t = self.text.text()
                t = float(t)
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "C":
            self.text.setText("")
        elif button == "Tan":
            try:
                t = float(self.text.text())
                t = Tan(t)
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "pi":
            self.text.setText(str(math.pi))
        elif button == "e":
            self.text.setText(str(math.e))
        elif button == "Sqrt":
            try:
                t = float(self.text.text())
                t = math.sqrt(t)
                self.text.setText(str(t))
            except Exception as e:
                print(e)
        elif button == "Ans":
            self.text.setText(str(self.result))
        else:
            t = self.text.text()
            t += button
            self.text.setText(t)


application = Calculator()        
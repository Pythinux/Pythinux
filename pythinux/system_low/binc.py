#!/usr/bin/python
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BinaryCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Binary Tally')
        self.icon = QIcon("../img/binary-tally.svg")
        self.setWindowIcon(self.icon)
        
        self.value = 0
        self.max_value = 2 ** 32 - 1  # Maximum value based on a 32-bit binary representation
        self.min_value = 0

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()

        self.value_label = QLabel('Value:')
        layout.addWidget(self.value_label)

        self.value_display = QLineEdit('0')
        self.value_display.setReadOnly(True)
        layout.addWidget(self.value_display)

        self.bits_label = QLabel('Number of Bits:')
        layout.addWidget(self.bits_label)

        self.bits_input = QLineEdit('8')
        layout.addWidget(self.bits_input)

        self.protect_checkbox = QCheckBox('Protect Against Over/Underflow')
        layout.addWidget(self.protect_checkbox)

        self.increment_button = QPushButton('Increment')
        self.increment_button.clicked.connect(self.increment_value)
        layout.addWidget(self.increment_button)

        self.decrement_button = QPushButton('Decrement')
        self.decrement_button.clicked.connect(self.decrement_value)
        layout.addWidget(self.decrement_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_value)
        layout.addWidget(self.reset_button)

        central_widget.setLayout(layout)
        
        self.update_display()
        
    def update_display(self):
        self.value_display.setText(format(self.value, '0' + self.bits_input.text() + 'b'))

    def increment_value(self):
        num_bits = int(self.bits_input.text())
        increment = 1
        if self.protect_checkbox.isChecked():
            increment = 1 if self.value < self.max_value else 0
        self.value = (self.value + increment) % (2 ** num_bits)
        self.update_display()

    def decrement_value(self):
        num_bits = int(self.bits_input.text())
        decrement = 1
        if self.protect_checkbox.isChecked():
            decrement = 1 if self.value > self.min_value else 0
        self.value = (self.value - decrement) % (2 ** num_bits)
        self.update_display()
    
    def reset_value(self):
        self.value = 0
        self.update_display()
    
application = BinaryCounterApp()
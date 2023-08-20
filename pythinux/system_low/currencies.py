from forex_python.converter import CurrencyRates
import forex_python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

global codes

codes = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE', 'CHF', 'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'N/A', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'USN', 'UYI', 'UYU', 'UYW', 'UZS', 'VED', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XBA', 'XBB', 'XBC', 'XBD', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'XSU', 'XTS', 'XUA', 'XXX', 'YER', 'ZAR', 'ZMW', 'ZWL']
class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base = QVBoxLayout()
        self.init_ui()
        self.setWindowTitle("Currencies")
        self.icon = QIcon("../img/coinbag.svg")
        self.setWindowIcon(self.icon)
    def init_ui(self):
        self.c = CurrencyRates()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        
        v = QDoubleValidator()
        
        self.fromInput = QLineEdit()
        self.fromInput.setPlaceholderText("Enter an amount")
        self.fromInput.setValidator(v)
        
        self.toInput = QLineEdit()
        self.toInput.setReadOnly(True)
        
        self.fromBox = QComboBox()
        for item in codes:
            self.fromBox.addItem(item)
        self.toBox = QComboBox()
        for item in codes:
            self.toBox.addItem(item)
            
        self.fromBox.setCurrentText("USD")
        self.toBox.setCurrentText("GBP")
        
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)
        
        self.base.addWidget(self.fromInput)
        self.base.addWidget(self.fromBox)
        self.base.addWidget(self.toBox)
        self.base.addWidget(self.button)
        self.base.addWidget(self.toInput)
        
        self.central.setLayout(self.base)
    def convert(self):
        if self.fromInput.text():
            self.toInput.setText("Converting...")
            a = float(self.fromInput.text())
            try:
                am = self.c.convert(self.fromBox.currentText(),self.toBox.currentText(),a)
            except Exception as e:
                am = str(e)
            self.toInput.setText(str(am))
    
application = Application()        
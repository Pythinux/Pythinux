#!/usr/bin/python
import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Define card-related constants
suits = ('H', 'D', 'C', 'S')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Define classes for cards, deck, and hands

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Define the GUI for the Blackjack game using PyQt5

class BlackjackApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blackjack")
        self.icon = QIcon("../img/crown.svg")
        self.setWindowIcon(self.icon)
        
        self.init_ui()

    def init_ui(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_label = QLabel("Player's Hand:")
        self.dealer_label = QLabel("Dealer's Hand:")
        self.info_label = QLabel("Welcome to Blackjack.")

        self.hit_button = QPushButton("Hit")
        self.stand_button = QPushButton("Stand")
        self.reset_button = QPushButton("New Game")

        self.hit_button.clicked.connect(self.player_hit)
        self.stand_button.clicked.connect(self.player_stand)
        self.reset_button.clicked.connect(self.reset_game)

        self.player_layout = QVBoxLayout()
        self.player_layout.addWidget(self.player_label)
        self.player_layout.addWidget(self.info_label)

        self.dealer_layout = QVBoxLayout()
        self.dealer_layout.addWidget(self.dealer_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.hit_button)
        self.button_layout.addWidget(self.stand_button)
        self.button_layout.addWidget(self.reset_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.dealer_layout)
        self.main_layout.addLayout(self.player_layout)
        self.main_layout.addLayout(self.button_layout)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.update_ui()

    def update_ui(self):
        player_cards = [f"{card.rank}{card.suit}" for card in self.player_hand.cards]
        dealer_cards = [f"{card.rank}{card.suit}" for card in self.dealer_hand.cards]
        
        c = []
        self.player_label.setText("Player's Hand: " + ", ".join(player_cards))
        self.dealer_label.setText("Dealer's Hand: " + ", ".join(dealer_cards[:1]))

        self.info_label.setText(f"Player's total: {self.player_hand.value}\nDealer's total: {self.dealer_hand.value}")

    def player_hit(self):
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.adjust_for_ace()
        self.update_ui()

        if self.player_hand.value > 21:
            self.player_stand()

    def player_stand(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.adjust_for_ace()

        self.update_ui()
        self.display_winner()

    def display_winner(self):
        if self.player_hand.value > 21:
            self.info_label.setText("Bust: {} > 21".format(self.player_hand.value))
        elif self.dealer_hand.value > 21 or self.player_hand.value > self.dealer_hand.value:
            self.info_label.setText("Congratulations! You win!")
        elif self.player_hand.value == self.dealer_hand.value:
            self.info_label.setText("It's a tie!")
        else:
            self.info_label.setText("Dealer wins. You lose!")

        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.reset_button.setEnabled(True)

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.reset_button.setEnabled(False)

        self.info_label.setText("Welcome to QBlackJack!")
        self.update_ui()

def main():
    app = QApplication(sys.argv)
    blackjack_app = BlackjackApp()
    blackjack_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
else:
    application = BlackjackApp()

import random

suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        deck_check = ''
        
        for card in self.deck:
            deck_check += '\n' + card.__str__()

        return 'The deck of cards contains: ' + deck_check
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        card = self.deck.pop()
        return card

class Hand():

    def __init__(self):
        self.aces = 0
        self.value = 0
        self.cards = []        

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


deck = Deck()
deck.shuffle()

player_hand = Hand()
player_hand.get_card(deck.deal_card())


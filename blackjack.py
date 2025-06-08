import random

suits = ('Diamonds', 'Hearts', 'Clubs', 'Spades')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King')

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six':6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10,
          'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_check = ''
        for card in self.deck:
            deck_check += '\n' + card.__str__()
        return 'The deck you are using has:' + deck_check
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

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

class ChipAccount:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("Place your bet! How many chips? "))

        except ValueError:
            print("You must enter an integer!")

        else:
            if chips.bet > chips.total:
                print("You don't have enough chips. You only have", chips.total)

            else:
                break

def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to hit or stand? Enter 'h' or 's': ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue

        break

def show_partial_cards(player, dealer):
    print("\nDealer's hand:")
    print(" *** ")
    print('', dealer.cards[1])
    print("\nPlayer's hand:", *player.cards, sep='\n')

def show_all_cards(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n')
    print("\nDealer's hand =", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n')
    print("\nPlayer's hand =", player.value)

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def tie(player, dealer):
    print("Dealer and Player tie!")


playing = True
player_chips = ChipAccount()

while True:
    print('''
    Welcome to 21! The aim of the game is to get as close to 21 
    without going over! The Deler will keep hitting until they reach 17.
    ''')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal()) 
    dealer_hand.add_card(deck.deal())

    take_bet(player_chips)

    show_partial_cards(player_hand, dealer_hand)

    while playing:

        hit_or_stand(deck, player_hand)

        show_partial_cards(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all_cards(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            tie(player_hand, dealer_hand)

    print("\nPlayer's winnings stand at", player_chips.total)

    new_game = input("Would you like to play another hand? Enter 'y' or 'n':")

    if new_game[0].lower() == 'y':
        playing = True
        continue

    else:
        print("Thanks for playing")
        break

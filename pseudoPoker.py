# GUI Elements:
# - PlayerPanel for each player showing their name, chips, current bet, and cards
# - CommunityCardsPanel showing the community cards
# - PotPanel showing the current size of the pot
# - ButtonPanel with buttons for each possible action (fold, call, raise)
# - LogPanel showing a log of all actions taken in the game

# Class Definitions:
# - Card: represents a playing card
# - Deck: represents a deck of cards, can deal cards and shuffle
# - Player: represents a player, has a name, number of chips, current bet, and a hand of cards
# - Game: represents the game, has a list of players, a deck, a pot, and the community cards

# Game Flow:
# - Initialize the GUI
# - Create a Game object with a list of Player objects
# - Enter the game loop
#     - For each round:
#         - Shuffle the deck
#         - Deal two cards to each player
#         - Update the PlayerPanels to show the players' cards and chip counts
#         - For each betting round:
#             - For each player:
#                 - Enable the ButtonPanel for the current player and disable it for all others
#                 - Wait for the player to press a button to choose their action
#                 - Update the PlayerPanel and PotPanel based on the player's action
#                 - Add the player's action to the LogPanel
#                 - If the player folds, remove them from the game
#             - If only one player remains, they win the pot and the round ends
#         - If the round continues past the betting rounds:
#             - Reveal the community cards
#             - Determine the winner based on the players' hands and the community cards
#             - The winner wins the pot
#             - Update the PlayerPanels and PotPanel
#     - If a player runs out of chips, they are removed from the game
#     - If only one player remains, they are the winner of the game


import tkinter as tk
from tkinter import scrolledtext
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from pypokerengine.utils.game_state_utils import restore_game_state, attach_hole_card, attach_hole_card_from_deck
from pypokerengine.utils.game_state_utils import attach_hole_card_from_deck, attach_hole_card, attach_hole_card_from_deck

# Define your PokerPlayer
class FishPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount
    # ... add other necessary methods ...

def start_game():
    config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
    config.register_player(name="p1", algorithm=FishPlayer())
    config.register_player(name="p2", algorithm=FishPlayer())
    config.register_player(name="p3", algorithm=FishPlayer())
    game_result = start_poker(config, verbose=1)
    # Display game_result on the GUI

def update_text_area(game_result):
    text_area.insert(tk.INSERT, str(game_result))

root = tk.Tk()
root.geometry('800x600')

# Add a button to start the game
start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack()

# Add a text area to display the game logs
text_area = scrolledtext.ScrolledText(root, width=100, height=40)
text_area.pack()

root.mainloop()

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for rank in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]:
                self.cards.append(Card(suit, rank))

    def show(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def deal(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 100
        self.bet = 0
        self.hand = []

    def __str__(self):
        return self.name + " has " + str(self.chips) + " chips and is betting " + str(self.bet) + " chips"

    def show_hand(self):
        for card in self.hand:
            print(card)

    def bet_chips(self, amount):
        self.chips -= amount
        self.bet += amount

    def win_chips(self, amount):
        self.chips += amount

    def clear_bet(self):
        self.bet = 0

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []

    def __str__(self):
        return "The pot is " + str(self.pot) + " chips"

    def deal(self):
        for player in self.players:
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())

    def show_hands(self):
        for player in self.players:
            print(player.name + "'s hand:")
            player.show_hand()

    def show_community_cards(self):
        for card in self.community_cards:
            print(card)

    def shuffle_deck(self):
        self.deck.shuffle()

    def clear_hands(self):
        for player in self.players:
            player.hand = []

    def clear_community_cards(self):
        self.community_cards = []

    def clear_pot(self):
        self.pot = 0

    def clear_bets(self):
        for player in self.players:
            player.clear_bet()

    def clear_game(self):
        self.clear_hands()
        self.clear_community_cards()
        self.clear_pot()
        self.clear_bets()

    def deal_flop(self):
        self.community_cards.append(self.deck.deal())
        self.community_cards.append(self.deck.deal())
        self.community_cards.append(self.deck.deal())

    def deal_turn(self):
        self.community_cards.append(self.deck.deal())

    def deal_river(self):
        self.community_cards.append(self.deck.deal())

    def bet_round(self):
        for player in self.players:
            print(player)
            print("The pot is " + str(self.pot))
            print("The community cards are:")
            self.show_community_cards()
            print("Your hand is:")
            player.show_hand()
            print("What would you like to do?")
            print("1. Fold")
            print("2. Call")
            print("3. Raise")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.players.remove(player)
            elif choice == "2":
                player.bet_chips(self.pot)
                self.pot += player.bet
            elif choice == "3":
                amount = int(input("How much would you like to raise? "))
                player.bet_chips(amount)
                self.pot += player.bet
            else:
                print("Invalid choice. Please try again.")
                self.bet_round()

    def play(self):
        self.shuffle_deck()
        self.deal()
        self.bet_round()
        self.deal_flop()
        self.bet_round()
        self.deal_turn()
        self.bet_round()
        self.deal_river()
        self.bet_round()
        self.show_hands()
        self.show_community_cards()

    def determine_winner(self):
        for player in self.players:
            print(player.name + "'s hand:")
            player.show_hand()
            print("The community cards are:")
            self.show_community_cards()
            print("The best hand is:")
            print(self.determine_best_hand(player))

    def determine_best_hand(self, player):
        best_hand = []
        for i in range(0, 5):
            best_hand.append(player.hand[i])
        for i in range(0, 5):
            best_hand.append(self.community_cards[i])
        best_hand.sort(key=lambda x: x.rank)
        print(best_hand)
        return best_hand

    def determine_hand_rank(self, player):
        hand = self.determine_best_hand(player)
        if self.is_royal_flush(hand):
            return 10
        elif self.is_straight_flush(hand):
            return 9
        elif self.is_four_of_a_kind(hand):
            return 8
        elif self.is_full_house(hand):
            return 7
        elif self.is_flush(hand):
            return 6
        elif self.is_straight(hand):
            return 5
        elif self.is_three_of_a_kind(hand):
            return 4
        elif self.is_two_pair(hand):
            return 3
        elif self.is_pair(hand):
            return 2
        else:
            return 1

    def is_royal_flush(self, hand):
        if self.is_straight_flush(hand) and hand[0].rank == 10:
            return True
        else:
            return False

    def is_straight_flush(self, hand):
        if self.is_flush(hand) and self.is_straight(hand):
            return True
        else:
            return False

    def is_four_of_a_kind(self, hand):
        if hand[0].rank == hand[1].rank == hand[2].rank == hand[3].rank:
            return True
        elif hand[1].rank == hand[2].rank == hand[3].rank == hand[4].rank:
            return True
        else:
            return False

    def is_full_house(self, hand):
        if hand[0].rank == hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
            return True
        elif hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank == hand[4].rank:
            return True
        else:
            return False

    def is_flush(self, hand):
        if hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit == hand[4].suit:
            return True
        else:
            return False

    def is_straight(self, hand):
        if hand[0].rank == hand[1].rank - 1 == hand[2].rank - 2 == hand[3].rank - 3 == hand[4].rank - 4:
            return True
        else:
            return False

    def is_three_of_a_kind(self, hand):
        if hand[0].rank == hand[1].rank == hand[2].rank:
            return True
        elif hand[1].rank == hand[2].rank == hand[3].rank:
            return True
        elif hand[2].rank == hand[3].rank == hand[4].rank:
            return True
        else:
            return False

    def is_two_pair(self, hand):
        if hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank:
            return True
        elif hand[0].rank == hand[1].rank and hand[3].rank == hand[4].rank:
            return True
        elif hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
            return True
        else:
            return False

    def is_pair(self, hand):
        if hand[0].rank == hand[1].rank:
            return True
        elif hand[1].rank == hand[2].rank:
            return True
        elif hand[2].rank == hand[3].rank:
            return True
        elif hand[3].rank == hand[4].rank:
            return True
        else:
            return False

    def show_hands(self):
        for player in self.players:
            print(player.name + "'s hand:")
            player.show_hand()

    def show_community_cards(self):
        for card in self.community_cards:
            print(card)


game = Game()
game.play()
game.determine_winner()



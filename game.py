import random, re

from domino import Domino
from player import Player
from board import Board

class Game:
    
    def __init__(self):
        self.player = Player()
        self.computer = Player()
        self.board = Board() 
        self.round = 1
        self.hands = 4           # 4 hands in 1 round
        self.start_new_round()
    
    
    # Resets game
    def start_new_round(self):
        self.white_set = []
        self.black_set = []
        
        self.create_dominos()     # Create the dominos, gives them to each player
        
        self.shuffle_dominos()    # Shuffles the dominos
        
        self.add_to_empty_board() # Adds the first 6 dominos (from each player) to the board
        
        self.play_round()         # Play a round of the game
        
        self.update_round_count() # Update the number of rounds played

    
    # Play a single round
    def play_round(self):
        # 1 hand means the players draw 6 (or 4) cards
        for hand in range(self.hands):
            self.draw(hand)
            player_finished = computer_finished = False
            while not player_finished: # or not computer_finished:
                if not player_finished:
                    player_finished = self.player_turn()
                # if not computer_finished:
                #     pass
                    # computer_finished = self.computer_turn()
            
        # self.start_new_round()
        
    
    def player_turn(self):
        self.board.print_stacks()
        self.player.print_hand()
        
        # The player is out of dominos to play
        if self.player.len_of_hand() == 0:
            print('No more cards to play')
            return True
        
        # Player makes a choice to play a domino or not
        choice = input('Would you like to place a domino? "Yes" or "No": ')
        if choice.lower() == "no":
            return True
        
        # Check to make sure domino is valid
        domino_name = ""
        while not self.player.domino_in_hand(domino_name):
            domino_name = input('Which domino from your hand do you want to play?: ')
        
        
        if self.player.domino_in_hand(domino_name):
            # Choose a valid position to put the domino
            position = -1
            while position > 12 or position < 1:
                position = input('Which stack do you want to add the domino to (1-12)?: ')
                if bool(re.search('[a-zA-Z]', position)):
                    position = -1
                position = int(position)
            
            # * Turn this into a loop so that the player doesnt lose his turn
            # Check the validity of the move
            if self.board.check_valid(domino, position):
                # Remove the domino from the players hand
                domino = self.player.remove_from_hand(domino_name)
                # Add domino to board
                self.board.add_domino_to_stack(domino, position)
            else:
                print('Invalid placement!')

        return False
    
    
    # Update to next round, if the player wants to play again
    def update_round_count(self):
        self.round += 1
        
    
    # Creates the dominos, and adds them to black and white set
    def create_dominos(self):
        seen = set()
        for i in range(7): 
            for j in range(7):
                if j == 0 and i > 0: continue
                if (j, i) in seen: continue 
                self.white_set.append(Domino(i, j, 'W'))
                self.black_set.append(Domino(i, j, 'B'))
                seen.add((i, j))
    
    
    # Shuffles the dominos in both sets    
    def shuffle_dominos(self):
        random.shuffle(self.white_set)
        random.shuffle(self.black_set)
    
    
    # Adds the first 6 cards from each shuffled sets to the board
    def add_to_empty_board(self):
        white_set = []
        for i in range(6):
            white_set.append(self.white_set.pop())
        self.board.add_to_empty_board(white_set, (0, 6))
        
        black_set = []
        for i in range(6):
            black_set.append(self.black_set.pop())
        self.board.add_to_empty_board(black_set, (6, 12))
    
    
    # Each player draws dominos, 6 if hands 1-3, 4 if hand 4
    def draw(self, hand):
        self.player.draw_hand(self.black_set, hand)
        self.computer.draw_hand(self.white_set, hand)
        self.player.move_to_graveyard(self.black_set)
        self.computer.move_to_graveyard(self.white_set)
    
    
    # Prints out dominos
    def print_dominos(self):
        for domino in self.black_set:
            print(domino)
    
    
    # Prints out hands
    def print_hands(self):
        print('PLAYER HAND')
        self.player.print_hand()
        print('COMPUTER HAND')
        self.computer.print_hand()
    
    
    # Prints out graveyards
    def print_graveyards(self):
        print('PLAYER GRAVEYARD')
        self.player.print_graveyard()
        print('COMPUTER GRAVEYARD')
        self.computer.print_graveyard()
import random, re, os

from domino import Domino
from player import Player
from board import Board
from computer import Computer

class Game:
    
    def __init__(self):
        self.player = Player()
        self.computer = Computer()
        self.board = Board() 
        self.round = 1
        self.hands = 4
    
    
    # Resets game
    def start_new_round(self):
        self.white_set = []
        self.black_set = []
        self.create_dominos()     # Create the dominos, gives them to each player
        self.shuffle_dominos()    # Shuffles the dominos
        self.add_to_empty_board() # Adds the first 6 dominos (from each player) to the board
        self.play_round()         # Play a round of the game
        self.update_round_count() # Update the number of rounds played
        
    
    def play(self):
        
        while True:
            self.start_new_round()
            choice = input('Would you like to play another round? "Yes" or "No": ')
            if choice.lower() == "no":
                break
        
        self.final_scores()

    
    def play_round(self):
        
        player_first = self.determine_turn_order()
        
        for hand in range(self.hands):
            self.draw(hand)
            player_finished = computer_finished = False
            while not player_finished and not computer_finished:
                if player_first:
                    if not player_finished:
                        player_finished = self.player_turn()
                    if not computer_finished:
                        computer_finished = self.computer_turn()
                else:
                    if not computer_finished:
                        computer_finished = self.computer_turn()
                    if not player_finished:
                        player_finished = self.player_turn()
                    
            # calculate each players score at the end of the hand
            self.calculate_scores()
            
        self.reveal_winner_of_round()
        
    
    def determine_turn_order(self):
        player_tile = self.black_set[0]
        computer_tile = self.white_set[0]
        
        player_first = player_tile.total_pips > computer_tile.total_pips
        if player_first:
            print(f'Player goes first with a score of {player_tile}')
        else:
            print(f'Computer goes first with a score of {computer_tile}')
        
        input('Press Enter to Continue...')
        
        return player_first
        
    
    def final_scores(self):
        player_wins = self.player.wins
        computer_wins = self.computer.wins
        
        if player_wins == computer_wins:
            print(f'COMPUTER AND PLAYER TIE THE TOURNAMENT WITH {player_wins} WINS')
        elif player_wins > computer_wins:
            print(f'PLAYER WINS THE TOURNAMENT WITH {player_wins} WINS')
        else:
            print(f'COMPUTER WINS THE TOURNAMENT WITH {computer_wins} WINS')
        
    
    def reveal_winner_of_round(self):
        player_score = self.player.score
        computer_score = self.computer.score
        if player_score == computer_score:
            print(f'ITS A TIE WITH A SCORE OF {player_score} FROM BOTH SIDES')
        elif player_score > computer_score:
            print(f'PLAYER WINS THE ROUND WITH A SCORE OF {player_score}')
            print(f'COMPUTER LOSES THE ROUND WITH A SCORE OF {computer_score}')
            self.player.increment_wins()
        else:
            print(f'COMPUTER WINS THE ROUND WITH A SCORE OF {computer_score}')
            print(f'PLAYER LOSES THE ROUND WITH A SCORE OF {player_score}')
            self.computer.increment_wins()
        
        
    
    def calculate_scores(self):
        player_score, computer_score = self.board.tally_scores()
        self.player.update_score(player_score)
        self.computer.update_score(computer_score)
        
        print(f'PLAYER CURRENT SCORE: {self.player.score}')
        print(f'COMPUTER CURRENT SCORE: {self.computer.score}')
    
    
    def check_hand_size(self):
        if self.player.size_of_hand() == 0:
            print('No more cards to play')
            return True
        return False
    
    
    def is_playing_round(self):
        choice = input('Would you like to place a domino? "Yes" or "No": ')
        if choice.lower() == "no":
            return True
        return False
    
    
    def get_domino_name(self):
        domino_name = ""
        while not self.player.domino_in_hand(domino_name):
            domino_name = input('Which domino from your hand do you want to play?: ')
        return domino_name
    
    
    def validate_position(self):
        position = -1
        while position > 12 or position < 1:
            position = input('Which stack do you want to add the domino to (1-12)?: ')
            if bool(re.search('[a-zA-Z]', position)):
                position = -1
            position = int(position)
        return position
    
    
    def clear_screen_then_print(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.board.print_stacks()
        print('Player: ')
        self.player.print_hand()
        self.player.print_graveyard()
        self.player.print_score()
        self.player.print_wins()
        print('Computer: ')
        self.computer.print_hand()
        self.computer.print_graveyard()
        self.player.print_score()
        self.player.print_wins()
        
        
    def ask_for_recommendation(self):
        choice = input('Would you like the Computer to recommend you a move? "Yes" or "No": ')
        if choice.lower() == "yes":
            self.computer.recommend_move(self.board, self.player.hand)
    
    
    def player_turn(self):
        input('Continue...')
        self.clear_screen_then_print()
        
        if self.check_hand_size():
            return True
        
        self.ask_for_recommendation()
        
        if self.is_playing_round():
            return True
        
        domino_name = self.get_domino_name()
        
        if self.player.domino_in_hand(domino_name):
            position = self.validate_position()
            domino = self.player.get_domino(domino_name)
            if not self.board.check_valid(domino, position):
                print('Invalid placement!')
                self.player_turn()
            
            if self.board.check_valid(domino, position):
                domino = self.player.remove_from_hand(domino_name)
                self.board.add_domino_to_stack(domino, position)

        return False
    
    
    def computer_turn(self):
        self.clear_screen_then_print()
        position, domino = self.computer.find_best_move(self.board)
        if (position is None and domino is None) or (self.computer.size_of_hand() == 0):
            return True
        self.computer.print_move(domino, position)
        self.board.add_domino_to_stack(domino, position + 1)
        self.computer.remove_from_hand(domino.display_name)
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
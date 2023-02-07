class Computer:
    def __init__(self):
        self.hand = []
        self.graveyard = []
        self.score = 0
        
    def find_best_move(self, board):
        best_tile = None
        best_position = 0  # Keeps track of which stack is best to add to 
        min_score = 100      # Keeps track of current best stack score
        top_tiles = [ tiles[-1] for tiles in board.stacks.values() ]
        
        # High score bad, low score good
        for position, board_domino in enumerate(top_tiles):
            for hand_domino in self.hand:
                if board.check_valid(hand_domino, position + 1):
                    score = abs(hand_domino.total_pips - board_domino.total_pips)
                    if board_domino.set_type == "W": 
                        score += 10
                    if score < min_score:
                        min_score = score
                        best_position = position
                        best_tile = hand_domino
                        
        if min_score >= 15:
            return (None, None)
        
        return (best_position, best_tile)
    
    def print_move(self, domino, position):
        print(f'Computer adds {domino} to tile stack {position + 1}')
        
    
    
    def size_of_hand(self):
        return len(self.hand)
    
    def draw_hand(self, domino_set, hand_cnt):
        num_of_cards = 6 if hand_cnt < 3 else 4
        i = 0
        while i < num_of_cards:
            self.hand.append(domino_set.pop())
            i += 1
                
    def move_to_graveyard(self, domino_set):
        self.graveyard = domino_set
        
    def domino_in_hand(self, domino_name):
        for domino in self.hand:
            if domino.display_name == domino_name:
                return True
        return False
    
    def remove_from_hand(self, domino_name):
        d = None
        for i, domino in enumerate(self.hand):
            if domino.display_name == domino_name:
                d = domino
                del self.hand[i]
        return d
    
    def get_domino(self, domino_name):
        d = None
        for i, domino in enumerate(self.hand):
            if domino.display_name == domino_name:
                d = domino
        return d
        
    def print_hand(self):
        print("Computer: ", end="")
        for domino in self.hand:
            print(domino, end=" ")
        print("")
    
    def print_graveyard(self):
        for domino in self.graveyard:
            print(domino)
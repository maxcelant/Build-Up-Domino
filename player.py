class Player:
    
    def __init__(self):
        self.hand = []
        self.graveyard = []
        self.score = 0
        
    def len_of_hand(self):
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
        
    def print_hand(self):
        print("Player: ", end="")
        for domino in self.hand:
            print(domino, end=" ")
        print("")
    
    def print_graveyard(self):
        for domino in self.graveyard:
            print(domino)
        
    
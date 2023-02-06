class Board:
    
    def __init__(self):
        # 0-5 are for the player (black), 6-11 are for computer (white)
        self.stacks = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[]}
        
    
    def add_to_empty_board(self, domino_set, stack_range):
        start, end = stack_range
        j = 0
        for i in range(start, end):
            self.stacks[i].append(domino_set[j])
            j += 1
            
    
    def add_domino_to_stack(self, domino, position):
        position = int(position)
        self.stacks[position-1].append(domino)
        
    def check_valid(self, domino, position):
        top_domino = self.stacks[position - 1][-1]
        # A non-double tile may be placed on any tile as long as the total number of pips on 
        # the tile played is equal to or greater than the tile being covered.
        if domino.total_pips > top_domino.total_pips:
            return True
        
        # A double may cover another double only if the covered tile has fewer total pips. 
        if domino.is_double and top_domino.is_double and domino.total_pips > top_domino.total_pips:
            return True
        
        # A double may cover any non-double tile, even if the covered tile has more pips
        if domino.is_double and not top_domino.is_double:
            return True
        
        return False
            
    
    def print_stacks(self):
        print('Stacks: ')
        for dominos in self.stacks.values():
            print(dominos[-1], end=" ")
        print("")
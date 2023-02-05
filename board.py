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
            
    
    def print_stacks(self):
        print('Stacks: ')
        for dominos in self.stacks.values():
            print(dominos[-1], end=" ")
        print("")
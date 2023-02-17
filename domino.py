class Domino:
    def __init__(self, left: int, right: int, set_type: str):
        self.left = left
        self.right = right
        self.set_type = set_type # W, B
        self.total_pips = left + right
        self.is_double = True if left == right else False
        self.display_name = f'{self.set_type}{self.left}{self.right}'
        
    
    def __str__(self):
        # (W 0:1)
        return self.display_name
    
    
    def __repr__(self):
        return str(self)
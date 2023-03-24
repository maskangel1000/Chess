class Piece:
    
    def __init__(self, color: chr, type: chr):
        self.color = color
        self.type = type
    
    def to_string(self):
        return self.color + self.type
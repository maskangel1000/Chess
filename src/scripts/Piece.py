class Piece:
    
    def __init__(self, color: str, type: str, x: int, y: int):
        self.color = color
        self.type = type
        self.x = x
        self.y = y
    
    def to_string(self):
        return self.color + self.type
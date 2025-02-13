
class Square:
    def __init__(self, row, col, score=0):
        self.row = row
        self.col = col
        self.score = score

class Shape:
    def __init__(self, squares):
        self.squares = squares
        self.width = 0
        self.height = 0

class Block:
    def __init__(self, row, col, score=0):
        self.row = row
        self.col = col
        self.score = score

class Shape:
    def __init__(self, blocks):
        #blocks is a list of blocks
        self.blocks = blocks
        self.width = 0
        self.height = 0
        self.borders = []
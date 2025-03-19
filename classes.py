import numpy as np


class Block:
    def __init__(self, row, col, score=0):
        self.row = row
        self.col = col
        self.score = score


class Shape:
    def __init__(self, segment):
        # segment is a list of blocks
        self.segment = segment
        self.width = 0
        self.height = 0
        self.borders = []

    def initialize(self):
        min_row = 100
        max_row = 0
        min_col = 100
        max_col = 0

        # Finding the dimensions of each shape
        for block in self.segment:
            if block.row < min_row:
                min_row = block.row
            if block.row > max_row:
                max_row = block.row
            if block.col < min_col:
                min_col = block.col
            if block.col > max_col:
                max_col = block.col

        self.width = max_col - min_col + 1
        self.height = max_row - min_row + 1

        # Shifting All shapes to the top left corner
        for block in self.segment:
            block.row -= min_row
            block.col -= min_col

        coords = []
        for block in self.segment:
            coords.append((block.row, block.col))
        # Define the borders of each shape, by checking the 4 adjacent positions
        for block in self.segment:
            if (block.row + 1, block.col) not in coords:
                self.borders.append(Block(block.row + 1, block.col))
                coords.append((block.row + 1, block.col))  # Preventing duplicates
            if (block.row - 1, block.col) not in coords:
                self.borders.append(Block(block.row - 1, block.col))
                coords.append((block.row - 1, block.col))
            if (block.row, block.col + 1) not in coords:
                self.borders.append(Block(block.row, block.col + 1))
                coords.append((block.row, block.col + 1))
            if (block.row, block.col - 1) not in coords:
                self.borders.append(Block(block.row, block.col - 1))
                coords.append((block.row, block.col - 1))

        self.segment.sort(key=sort_blocks)
        self.borders.sort(key=sort_blocks)

        # print("Squares", [(square.row, square.col) for square in self.segment])
        # print("Borders", [(square.row, square.col) for square in self.borders])


def sort_blocks(block):
    return (block.row, block.col)


def sort_turns(turn):
    return turn.score


class GameTurn:
    def __init__(self, order, score=0, board=np.zeros((8, 8))):
        self.order = order
        self.positions = [0, 0, 0]
        self.score = score
        self.board = board

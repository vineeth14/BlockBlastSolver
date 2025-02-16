import numpy as np

def check_color(measured, reference, allowed_deviation):
    correct = True
    for i in range(3):
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            correct = False
    return correct

class Block:
    def __init__(self, row, col, score=0):
        self.row = row
        self.col = col
        self.score = score

class Shape:
    def __init__(self, squares):
        self.squares = squares
        self.width = 0
        self.height = 0
        self.borders = []
        self.click_x = 0
        self.click_y = 0
        self.release_x = 0
        self.release_y = 0

    def initialize(self):
        # Defines the pixel where to click to move the shape
        # When clicking on a shape, the center (both row and col) moves from the invisible center line of the 3 shapes to the bottom border of the screen
        # Invisible line at y=1355, bottom border (which corresponds to piece center) is at 1145
        # So when clicking at the center of the shape, the new piece center is 210 pixels higher
        x_min = 1025
        y_min = 1240
        offset = 41
        x0 = 30

        min_row = 100
        max_row = 0
        min_col = 100
        max_col = 0
        for square in self.squares:
            if square.row < min_row:
                min_row = square.row
            if square.row > max_row:
                max_row = square.row
            if square.col < min_col:
                min_col = square.col
            if square.col > max_col:
                max_col = square.col

        self.width = max_col - min_col + 1
        self.height = max_row - min_row + 1
        self.click_x = x_min + (min_col * offset + x0) + self.width * offset // 2  # bbox start + leftmost pixel + half width
        self.click_y = y_min + (min_row * offset) + self.height * offset // 2  # bbox start + topmost pixel + half width

        # To have coordinates starting from 0,0 in the top left corner of the shape
        for square in self.squares:
            square.row -= min_row
            square.col -= min_col

        # Define border squares
        coords = [(square.row, square.col) for square in self.squares]
        for square in self.squares:
            if (square.row + 1, square.col) not in coords:
                self.borders.append(Square(square.row + 1, square.col))
                coords.append((square.row + 1, square.col))
            if (square.row - 1, square.col) not in coords:
                self.borders.append(Square(square.row - 1, square.col))
                coords.append((square.row - 1, square.col))
            if (square.row, square.col + 1) not in coords:
                self.borders.append(Square(square.row, square.col + 1))
                coords.append((square.row, square.col + 1))
            if (square.row, square.col - 1) not in coords:
                self.borders.append(Square(square.row, square.col - 1))
                coords.append((square.row, square.col - 1))

        self.squares.sort(key=sort_squares)
        self.borders.sort(key=sort_squares)

    def display(self):
        print("Squares", [(square.row, square.col) for square in self.squares])
        print("Borders", [(square.row, square.col) for square in self.borders])

def sort_squares(square):
    return (square.row, square.col)

def sort_positions(square):
    return square.score

def sort_score_positions(score):
    return score[0]

def sort_turns(turn):
    return turn.score

class GameTurn:
    def __init__(self, order, score=0, board=np.zeros((8, 8))):
        self.order = order
        self.positions = [0, 0, 0]
        self.score = score
        self.board = board

    def display(self):
        print(self.order, [(square.row, square.col, square.score) for square in self.positions], self.score)
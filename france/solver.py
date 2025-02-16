from PIL import Image, ImageGrab
from time import sleep, time
import pyautogui  # Required for proper positioning functionality
from pynput.mouse import Button, Controller
from itertools import permutations
from game_core import Block, Shape, GameTurn, check_color
import numpy as np

mouse = Controller()

def read_board():
    x_min = 1015
    y_min = 434
    x_max = 1722
    y_max = 1142
    im = ImageGrab.grab(bbox=(x_min, y_min, x_max, y_max))
    px = im.load()
    offset = 89  # distance between 2 empty blocks of the grid
    row0 = 45  # ~ offset//2
    col0 = 45  # ~ offset//2
    ref_background = (35, 45, 85)  # rgb value of background pixels of the grid
    board = np.zeros((8, 8)) 
    for row in range(8):
        for col in range(8):
            if not check_color(px[row * offset + row0, col * offset + col0], ref_background, 0.1):
                board[col, row] = 1
    return board

def read_grid():
    x_min = 1025
    y_min = 1240
    x_max = 1710
    y_max = 1468
    im = ImageGrab.grab(bbox=(x_min, y_min, x_max, y_max))
    px = im.load()
    offset = 41  # distance between two blocks
    x0 = 10  # can be adapted to the screen dimensions
    x = -1
    ref_background = (48, 74, 139)
    grid = np.zeros(((y_max - y_min) // offset + 2, (x_max - x_min) // offset + 2))  # the 2 may be changed for fine tuning of pixels
    while (x + 1) * offset + x0 < (x_max - x_min) - 1:
        x += 1
        y = 0
        is_background = True
        while (y + 1) * offset < (y_max - y_min) - 1:
            y += 1
            color_check = check_color(px[x * offset + x0, y * offset], ref_background, 0.1)
            if is_background and not color_check:  # on background but not background color = not on background
                is_background = False
                grid[y, x] = 1
            elif not color_check:  # not on background and not background color = still not on background
                grid[y, x] = 1
            elif not is_background:  # not on background but background color = back on background
                break
    return grid

def create_shapes(grid):
    shapes = []
    possible_squares = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1:
                # Get coordinates of each 1 in the shape
                grid[row, col] = 0
                origin = Block(row, col)
                edges = [origin]
                shape = Shape([origin])
                shapes.append(shape)
                while len(edges) > 0:
                    new = []
                    for square in edges:
                        for possible in possible_squares:
                            drow, dcol = possible[0], possible[1]
                            if (square.row + drow < grid.shape[0] and 
                                square.col + dcol < grid.shape[1] and 
                                square.row + drow >= 0 and 
                                square.col + dcol >= 0 and 
                                grid[square.row + drow, square.col + dcol] == 1):
                                grid[square.row + drow, square.col + dcol] = 0
                                shape.squares.append(Block(square.row + drow, square.col + dcol))
                                new.append(Block(square.row + drow, square.col + dcol))
                    edges = new[:]
                shape.initialize()
    return shapes

def count_holes(board):
    holes = []
    possible_squares = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for row in range(8):
        for col in range(8):
            if board[row, col] == 0:
                board[row, col] = 1
                frontier = [Block(row, col)]
                count = 1
                while len(frontier) > 0:
                    new = []
                    for square in frontier:
                        for possible in possible_squares:
                            drow, dcol = possible[0], possible[1]
                            if (square.row + drow < 8 and 
                                square.col + dcol < 8 and 
                                square.row + drow >= 0 and 
                                square.col + dcol >= 0 and 
                                board[square.row + drow, square.col + dcol] == 0):
                                board[square.row + drow, square.col + dcol] = 1
                                new.append(Block(square.row + drow, square.col + dcol))
                                count += 1
                    frontier = new[:]
                holes.append(count)
    return holes

def position_shapes(board, shapes):
    # For each possible order, we go through the 3 numbers, and for each number we test all possible placements
    # coming from the previous number. This allows testing all possibilities of placing the 3 shapes
    original_board = np.copy(board)
    turns = []  # all possible placements of 3 shapes for all possible orders
    # When 2 shapes are identical we can divide the number of possibilities by 2
    already_seen = []
    fill_count = np.count_nonzero(board)
    
    for order in permutations(range(3)):
        seen = False
        for permut in already_seen:
            count = 0
            for i in range(3):
                if [(square.row, square.col) for square in shapes[permut[i]].squares] == [(square.row, square.col) for square in shapes[order[i]].squares]:
                    count += 1
            if count == 3:
                print("Identical order (2 identical shapes)")
                seen = True
                break
        if seen:
            continue
        already_seen.append(order)
        
        current_turn = GameTurn(order)
        current_turn.board = np.copy(original_board)
        possible = True
        order_turns = [current_turn]
        
        for number in order:
            number_turns = []
            shape = shapes[number]
            for turn in order_turns:
                square_turns = []
                for row in range(8 - shape.height + 1):
                    for col in range(8 - shape.width + 1):
                        # Check if space is taken
                        skip = False
                        for square in shape.squares:
                            if turn.board[row + square.row, col + square.col] == 1:
                                skip = True
                                break
                        if skip:
                            continue
                            
                        test_board = np.copy(turn.board)
                        # Calculate score based on neighbors
                        score = 0
                        for square in shape.borders:
                            if row + square.row == -1 or row + square.row == 8 or col + square.col == -1 or col + square.col == 8:
                                score += 1
                            else:
                                score += test_board[row + square.row, col + square.col]
                                
                        # Place the piece
                        for square in shape.squares:
                            test_board[row + square.row, col + square.col] = 1
                            
                        # Remove full columns and increase score
                        bonus = 30
                        rows, cols = [], []
                        for c in range(8):
                            if sum(test_board[r, c] for r in range(8)) == 8:
                                score += bonus
                                cols.append(c)
                                
                        # Remove full rows and increase score
                        for r in range(8):
                            if sum(test_board[r, c] for c in range(8)) == 8:
                                score += bonus
                                rows.append(r)
                                
                        for c in cols:
                            for r in range(8):
                                test_board[r, c] = 0
                        for r in rows:
                            for c in range(8):
                                test_board[r, c] = 0
                                
                        # Favor filling rows and columns
                        coeff = 2  # coefficient must be greater than 1 for multiplicative effect on row/col completion
                        for c in range(8):
                            score += sum(board[r, c] for r in range(8)) * coeff
                            score += sum(board[c, r] for r in range(8)) * coeff
                            
                        # Penalize creation of single square blocks
                        coeff = 6
                        possible_squares = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                        for r in range(8):
                            for c in range(8):
                                if test_board[r, c] == 1:
                                    neighbors = 0
                                    for square in possible_squares:
                                        if (square[0] + r >= 8 or 
                                            square[1] + c >= 8 or 
                                            square[0] + r < 0 or 
                                            square[1] + c < 0 or 
                                            test_board[square[0] + r, square[1] + c] == 0):
                                            neighbors += 1
                                    if neighbors > 3:
                                        score -= neighbors * coeff

                        # Penalize holes
                        coeff = 2
                        holes = count_holes(np.copy(test_board))
                        for hole in holes:
                            score -= (len(holes) - 1) * 1 / hole * coeff

                        test_turn = GameTurn(order, score + turn.score, np.copy(test_board))
                        test_turn.positions = turn.positions[:]
                        test_turn.positions[number] = Block(row, col, score)
                        square_turns.append(test_turn)
                        
                if len(square_turns) == 0:
                    # Not possible to place this block
                    continue
                    
                seen_boards = []
                seen_scores = []
                for square_turn in square_turns:
                    # To reduce the number of situations to try, we remove operations that give the same result
                    # Don't do it with score as 2 different boards can have the same score
                    
                    # Testing all possibilities is too slow and unnecessary if there are few squares
                    if fill_count > 15:
                        number_turns.append(square_turn)
                    else:
                        # Here we do it with score because when there are few squares it's too long to test all possibilities
                        skip = False
                        for seen in seen_scores:
                            if seen == square_turn.score:
                                skip = True
                                break
                        if not skip:
                            number_turns.append(square_turn)
                            seen_scores.append(square_turn.score)

            if len(number_turns) == 0:
                print("impossible")
                possible = False
                break
            order_turns = number_turns[:]
            
        if possible:
            for turn in order_turns:
                turns.append(turn)
                
    # Select board with best score
    if len(turns) > 0:
        turns.sort(reverse=True, key=sort_turns)
        print(f"{len(turns)} possible boards")
        return turns[0]
    else:
        return "Lost"

def move_shapes(turn, shapes):
    # Calculate where to release the shape
    offset = 89  # distance between 2 empty blocks of the grid
    x0, y0 = 1015, 435  # same as x_min and y_min of read_board()
    vertical_gap = 210  # maybe the change in position of the shape when clicking on it, which gives a hovering effect above the board
    
    for number in turn.order:
        shape = shapes[number]
        shape.release_x = (x0 + turn.positions[number].col * offset) + shape.width * offset // 2 + 35  # 35 could be adjusted
        shape.release_y = (y0 + turn.positions[number].row * offset) + shape.height * offset // 2 + vertical_gap + 10  # 10 could be adjusted
        
        mouse.position = (shape.click_x, shape.click_y)
        sleep(0.4)
        mouse.press(Button.left)
        sleep(0.5)
        
        a = (shape.release_y - shape.click_y) / (shape.release_x - shape.click_x)
        b = shape.click_y - a * shape.click_x
        dx = (shape.release_x - shape.click_x) / abs(shape.release_x - shape.click_x) * min(1, abs(1/a)) * 12  # 12 ?
        
        x, y = shape.click_x, shape.click_y
        while y > shape.release_y:
            x += dx
            y = a * x + b
            mouse.position = (x, y)
            sleep(0.00001)
            
        sleep(0.5)
        mouse.release(Button.left)
        mouse.position = (955, 1226)  # anywhere outside the screen as to not have an effect on the reading of the screen

# Main
finished = False
sleep(1)  # defines the time in seconds between running the screen and the time it will start reading the screen
board = read_board()

while not finished:
    grid = read_grid()
    shapes = create_shapes(grid)
    if len(shapes) != 3:
        raise Exception(f"{len(shapes)}/3 proposed blocks detected")
    for shape in shapes:
        shape.display()
    turn = position_shapes(board, shapes)
    if isinstance(turn, str):
        print('No possible solution')
        finished = True
    else:
        board = np.copy(turn.board)
        print(board)
        move_shapes(turn, shapes)
        sleep(1)
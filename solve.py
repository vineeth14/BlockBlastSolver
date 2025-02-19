from classes import Block, Shape, GameTurn
from image_select import read_shapes_to_grid, image_to_grid
from itertools import permutations
import numpy as np

def create_shapes(grid):
    shapes = []
    directions = [[0,1],[1,0],[1,1],[-1,-1],[1,-1],[-1,1],[-1,0],[0,-1]]
    #BFS to find all shapes in the grid
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] == 1:
                grid[row][col] = 0
                origin = Block(row,col)
                shape = Shape([origin])
                q = [origin]
                shapes.append(shape)
                while len(q)>0:
                    for i in range(len(q)):
                        block = q.pop()
                        for dr,dc in directions:
                            nr, nc = dr+block.row, dc+block.col
                            if nr in range(grid.shape[0]) and nc in range(grid.shape[1]) and grid[nr][nc] == 1:
                                grid[nr][nc] = 0
                                q.append(Block(nr,nc))
                                shape.segment.append(Block(nr,nc))
                shape.initialize()
    print(len(shapes))
    return shapes

def count_holes(board):
    holes = []
    directions = [[0,1],[1,0],[0,-1],[-1,0]]
    for row in range(8):
        for col in range(8):
            if board[row][col] == 0:
                board[row][col] = 1
                origin = Block(row,col)
                count = 1
                q = [origin]
                while len(q) > 0:
                    for i in range(len(q)):
                        block = q.pop()                    
                        for dr,dc in directions:
                            nr, nc = dr+block.row, dc+block.col
                            if nr in range(8) and nc in range(8) and board[nr][nc] == 0:
                                board[nr][nc] = 1
                                q.append(Block(nr,nc))
                                count += 1
                holes.append(count)
    return holes

def solve_board(board,shapes):
    originalBoard = np.copy(board)
    turns = []
    alreadySeen = []
    fill_count = np.count_nonzero(board)


    for order in permutations(range(3)):
        seen = False
        for permut in alreadySeen:
            count = 0
            for i in range(3):
                #If they are the same, it means that at position i the shape is identical (in terms of its blocks) between the two permutations.
                if [(block.row,block.col) for block in shapes[permut[i]].segment] == [(block.row,block.col) for block in shapes[order[i]].segment]:
                    count+=1
                if count == 3:
                    # if Count is 3 then at all 3 indexes the shapes are identical
                    seen = True
                    break
        if seen:
            continue
        alreadySeen.append(order)

        currentTurn = GameTurn(order)
        orderTurn = [currentTurn]
        currentTurn.board = np.copy(originalBoard)

        for number in order:
            number_turns = []
            shape = shapes[number]
            for turn in orderTurn:
                block_turns = []
                for r in range(8-shape.width+1):
                    for c in range(8-shape.height+1):
                        skip=False
                        for block in shape.segment:
                            if turn.board[r+block.row][c+block.col]==1:
                                skip=True
                                break
                        if skip:
                            continue
                        tempBoard = np.copy(originalBoard)
                        score = 0
                        for block in shape.segment:
                            if r+block.row == -1 or r+block.row == 8 or c+block.col == -1 or c+block.col == 8:
                                score+=1
                            else:
                                score+=tempBoard[r+block.row][c+block.col] #isn't this just 0?
                        for block in shape.segment:
                            tempBoard[r+block.row][c+block.col]=1

                        bonus = 30
                        columns,rows = [],[]

                        for c_idx in range(8):
                            if sum(tempBoard[r_idx][c_idx] for r_idx in range(8)) == 8 :
                                score+=bonus
                                columns.append(c_idx)
                        
                        for r_idx in range(8):
                            if sum(tempBoard[r_idx][c_idx] for c_idx in range(8)) == 8:
                                score+=bonus
                                rows.append(r_idx)
                        
                        # Clear completed rows/columns
                        for c_idx in columns:
                            for r_idx in range(8):
                                tempBoard[r_idx, c_idx] = 0
                        for r_idx in rows:
                            for c_idx in range(8):
                                tempBoard[r_idx, c_idx] = 0

                        # # Score progress toward completing rows/columns
                        #     coeff = 2
                        #     for c in range(8):
                        #         score += sum(board[r, c] for r in range(8)) * coeff
                        #         score += sum(board[c, r] for r in range(8)) * coeff
                            
                        # Penalize isolated squares
                        coeff = 6
                        possible_blocks = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                        for r_idx in range(8):
                            for c_idx in range(8):
                                if tempBoard[r_idx, c_idx] == 1:
                                    neighbors = 0
                                    for block in possible_blocks:
                                        if (block[0]+r_idx not in range(8) or block[1]+c_idx not in range(8) or 
                                            tempBoard[block[0] + r_idx][block[1] + c_idx] == 0):
                                            neighbors += 1
                                    if neighbors > 3:
                                        score -= neighbors * coeff

                        # Penalize holes
                        coeff = 2
                        holes = count_holes(np.copy(tempBoard))
                        for hole in holes:
                            score -= (len(holes) - 1) * 1 / hole * coeff

                        # Create new turn with this placement
                        newTurn = GameTurn(order, score + turn.score, np.copy(tempBoard))
                        newTurn.positions = turn.positions[:]
                        newTurn.positions[number] = Block(r, c, score)
                        block_turns.append(newTurn)
                    
                                    

                            

            
        




grid = read_shapes_to_grid('uncompressed_images/IMG_0437.PNG')
shapes = create_shapes(grid)

board = image_to_grid('uncompressed_images/IMG_0437.PNG')
# print(board)
holes = count_holes(board)
# print(holes)
solve_board(board,shapes)
 

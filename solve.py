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
        currentTurn.board = np.copy(originalBoard)
        orderTurn = [currentTurn]
        for number in order:

            for turn in orderTurn:
                shape = shapes[number]
                moves = []
                for row_idx in range(8-shape.width+1):
                    for col_idx in range(8-shape.height+1):
                        skip=False
                        for block in shape.segment:
                            if currentTurn.board[row_idx+block.row][col_idx+block.col]==1:
                                skip=True
                                break
                        if skip:
                            continue
                
                        tempBoard = np.copy(currentTurn.board)
                        score = 0

                        #checking if the previous computed block's border + the current coords are still touching the border
                        for block in shape.borders:
                            if row_idx+block.row not in range(8) or col_idx+block.col not in range(8):
                                score +=1
                            else:
                                #Adding score if the shape is touching other blocks
                                score+=tempBoard[row_idx+block.row][col_idx+block.col]
                        
                        for block in shape.segment:
                            tempBoard[row_idx+block.row][col_idx+block.col]=1


                        #Finding Completed Columns and Rows and rewarding bonus points
                        bonus = 30 
                        rows,columns = [], []
                        for r in range(8):
                            if sum(tempBoard[r][c] for c in range(8)) == 8:
                                   score += bonus
                                   rows.append(r)
                        for c in range(8):
                            if sum(tempBoard[r][c] for r in range(8)) == 8:
                                score += bonus
                                columns.append(c)


                        # Clearing Rows and Columns
                        for c in columns:
                            for r in range(8):
                                tempBoard[r][c] = 0
                        for r in rows:
                            for c in range(8):
                                tempBoard[r][c] = 0
                        
                        #Board is now in state after piece is placed and completed row and column are removed
                        
                        #Scoring partially completed rows/columns
                        coeff = 2
                        for r in range(8):
                            score += sum(tempBoard[r][c] for c in range(8)) * coeff
                        for c in range(8):
                            score += sum(tempBoard[r][c] for r in range(8)) * coeff

                        #Penalize isolated blocks
                        coeff = 6
                        directions = [[-1,0],[0,1],[1,0],[0,-1]]
                        for r in range(8):
                            for c in range(8):
                                if tempBoard[r][c] == 1:
                                    empty_space = 0
                                    for dir in directions:
                                        nr,nc =d ir[0] + r, dir[1] + c
                                        if nr not in range(8) or nc not in range(8) or tempBoard[nr][nc] == 0:
                                            empty_space += 1
                                    if empty_space > 3:
                                        score -= empty_space* coeff
                        
                        #Penalize Holes
                        coef = 2
                        holes = count_holes(np.copy(tempBoard))
                        for hole in holes:
                            score -= (len(holes) - 1) * 1 / hole * coeff

                        # Create new turn with this placement
                        new_turn = GameTurn(order, score + turn.score, np.copy(tempBoard))
                        new_turn.positions = turn.positions[:]
                        new_turn.positions[number] = Block(row_idx, col_idx, score)
                        moves.append(new_turn)
                                        


                        
                        

            
        




grid = read_shapes_to_grid('uncompressed_images/IMG_0437.PNG')
shapes = create_shapes(grid)

board = image_to_grid('uncompressed_images/IMG_0437.PNG')
# print(board)
holes = count_holes(board)
# print(holes)
solve_board(board,shapes)
 

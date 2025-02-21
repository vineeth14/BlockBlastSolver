#!/usr/bin/env python3
from classes import Block, Shape, GameTurn, sort_turns
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

    return shapes

def count_holes(board):
    holes = []
    directions = [[0,1],[1,0],[0,-1],[-1,0]]
    #BFS to find all holes in the board
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
    completedGames = []
    alreadySeen = []
    fillCount = np.count_nonzero(board)
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

        # Initialize turn for current order
        currentTurn = GameTurn(order)
        currentTurn.board = np.copy(originalBoard)
        boardStates = [currentTurn] #List of all valid board states
        possible = True

        #Testing each shape in current order
        for number in order:
            shape = shapes[number]
            acceptedMoves = [] #Aggregated candidate moves across all board states for the current shape.

            #For each valid board state we must try all order of shape placement (BFS)
            for turn in boardStates:
                validPlacements = [] #Temporary collection of all valid moves found when trying to place the current shape at different positions on a single board state

                #Loop through all possible positions on the board for the current shape
                for row_idx in range(8-shape.height+1):
                    for col_idx in range(8-shape.width+1):
                        skip=False
                        #Checking each position on the board
                        for block in shape.segment:
                            if turn.board[row_idx+block.row][col_idx+block.col]==1:
                                skip=True
                                break
                        if skip:
                            continue
                        
                        #Score Calculation
                        tempBoard = np.copy(turn.board) #board to make changes against after placing shape
                        score = 0

                        #Placing shape
                        for block in shape.segment:
                            tempBoard[row_idx+block.row][col_idx+block.col]=1

                        #Checking if the computed block's border is touching the border of the grid.
                        for block in shape.borders:
                            if row_idx+block.row not in range(8) or col_idx+block.col not in range(8):
                                score +=1
                            else:
                                #Adding score if the shape is touching other blocks
                                score+=tempBoard[row_idx+block.row][col_idx+block.col]

                        #Finding Completed Columns and Rows and rewarding bonus points
                        bonus = 50
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
                        #Rewarding bc partially completed rows are desirable
                        # coeff = 2
                        # for r in range(8):
                        #     filled = sum(tempBoard[r][c] for c in range(8)) * coeff
                        #     score += filled 
                        # for c in range(8):
                        #     filled = sum(tempBoard[r][c] for r in range(8)) * coeff
                        #     score += filled 

                        #Penalize isolated blocks
                        coeff = 6
                        directions = [[-1,0],[0,1],[1,0],[0,-1]]
                        for r in range(8):
                            for c in range(8):
                                if tempBoard[r][c] == 1:
                                    emptySpace = 0
                                    for dir in directions:
                                        nr,nc = dir[0] + r, dir[1] + c
                                        if nr not in range(8) or nc not in range(8) or tempBoard[nr][nc] == 0:
                                            emptySpace += 1
                                    if emptySpace > 3:
                                        score -= emptySpace* coeff
                        
                        #Penalize Holes
                        coef = 2
                        holes = count_holes(np.copy(tempBoard))
                        for hole in holes:
                            score -= (len(holes) - 1) * 1 / hole * coeff

                        # Create new turn with this placement 
                        newTurn = GameTurn(order, score + turn.score, np.copy(tempBoard))
                        newTurn.positions = turn.positions[:] #shallow copy
                        # Storing positions of shape with score
                        newTurn.positions[number] = Block(row_idx, col_idx, score)
                        validPlacements.append(newTurn)
                # Done processing the board with all 3 shapes and permutations. 

                if len(validPlacements) == 0 :
                    # No valid Moves
                    continue
                
                seenScore = []
                for placement in validPlacements:
                    if fillCount>15: #Could change this to make it faster (need to test)
                        acceptedMoves.append(placement)
                    else:
                        # Skipping boards(valid placements) with same score because when we have a relatively emtpy board, 
                        # we don't need to consider every valid placement with the same score.
                        skip = False
                        for seen in seenScore:
                            if seen == placement.score:
                                skip = True
                                break
                        if not skip:
                            acceptedMoves.append(placement)
                            seenScore.append(placement.score)

            if len(acceptedMoves) == 0:
                print("impossible")
                possible = False
                break
            #Updating board states with acceptedMoves before next shape
            boardStates = acceptedMoves[:]

        #If possible to place 3 shapes, boardStates will contain a list of GameTurn objects
        # representing all possible ways to place the 3 shapes on the board.
        if possible:
            for turn in boardStates:
                completedGames.append(turn)

    if len(completedGames) > 0:
        #Sorting the turns by score in descending order
        completedGames.sort(reverse=True, key=sort_turns)
        print(f"{len(completedGames)} possible boards")
        return completedGames[0]
    else:
        return "Lost"
                        
                        
def generate_step_boards(board, shapes, winning_turn):
    step_boards = []
    completion_counter = {1:[],2:[],3:[]}
    current_board = np.copy(board)
    # For each shape in the winning order
    for step, shape_idx in enumerate(winning_turn.order, 1):  # start=1 to use 1,2,3 as markers
        # Create a new board for this step
        step_board = np.copy(current_board)
        position = winning_turn.positions[shape_idx]
        
        # Place the shape at its position using the step number (1,2,3) instead of 1
        for block in shapes[shape_idx].segment:
            step_board[position.row + block.row][position.col + block.col] = step+1
            
        step_boards.append(step_board)
        current_board = np.copy(step_board)
        
        # Clear any completed rows and columns
        completed_rows = 0
        completed_columns = 0
        rows, columns = [], []
        for r in range(8):
            if sum(bool(current_board[r][c]) for c in range(8)) == 8:  # using bool() to count any non-zero value
                rows.append(r)
                completed_rows += 1
        for c in range(8):
            if sum(bool(current_board[r][c]) for r in range(8)) == 8:
                columns.append(c)
                completed_columns += 1
        # Clear them
        completion_counter[step].append([completed_rows,completed_columns])
        for c in columns:
            for r in range(8):
                current_board[r][c] = 0
        for r in rows:
            for c in range(8):
                current_board[r][c] = 0
    print(completion_counter)
    return completion_counter, step_boards


#!/usr/bin/env python3
from classes import Block, Shape, GameTurn, sort_turns
from image_select import read_shapes_to_grid, image_to_grid
from itertools import permutations
import numpy as np

BOARD_SIZE = 8
BONUS_POINTS = 50
ISOLATION_PENALTY_COEFF = 6
HOLE_PENALTY_COEFF = 2
FILL_COUNT_THRESHOLD = 15

ADJACENT_DIRECTIONS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
ALL_DIRECTIONS = [[0, 1], [1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1], [-1, 0], [0, -1]]


def create_shapes(grid):
    """
    Performs BFS to find shapes in the input grid and create corresponding shape objects.
    """
    shapes = []
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] == 1:
                grid[row][col] = 0
                origin = Block(row, col)
                shape = Shape([origin])
                q = [origin]
                shapes.append(shape)
                while len(q) > 0:
                    for i in range(len(q)):
                        block = q.pop()
                        for dr, dc in ALL_DIRECTIONS:
                            nr, nc = dr + block.row, dc + block.col
                            if (
                                nr in range(grid.shape[0])
                                and nc in range(grid.shape[1])
                                and grid[nr][nc] == 1
                            ):
                                grid[nr][nc] = 2
                                q.append(Block(nr, nc))
                                shape.segment.append(Block(nr, nc))
                shape.initialize()

    return shapes


def count_holes(board):
    """
    Performs BFS to identify and count all holes in the board.
    A hole is defined as a connected region of empty cells.
    """
    holes = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                board[row][col] = 1
                origin = Block(row, col)
                count = 1
                q = [origin]
                while len(q) > 0:
                    for i in range(len(q)):
                        block = q.pop()
                        for dr, dc in ADJACENT_DIRECTIONS:
                            nr, nc = dr + block.row, dc + block.col
                            if (
                                nr in range(BOARD_SIZE)
                                and nc in range(BOARD_SIZE)
                                and board[nr][nc] == 0
                            ):
                                board[nr][nc] = 1
                                q.append(Block(nr, nc))
                                count += 1
                holes.append(count)
    return holes


def is_permutation_seen(order, already_seen, shapes):
    """
    Checks if a permutation of shapes has already been processed.
    If they are the same, it means that at position i the shape is identical (in terms of its blocks) between the two permutations.
    """
    for permut in already_seen:
        matching_shapes = 0
        for i in range(3):
            current_shape = [
                (block.row, block.col) for block in shapes[order[i]].segment
            ]
            permut_shape = [
                (block.row, block.col) for block in shapes[permut[i]].segment
            ]
            if current_shape == permut_shape:
                matching_shapes += 1
        if matching_shapes == 3:
            return True
    return False


def try_place_shape(board, shape, row_idx, col_idx):
    """
    Checks if a shape can be placed at the specified position on the board.
    """
    for block in shape.segment:
        if board[row_idx + block.row][col_idx + block.col] == 1:
            return False
    return True


def calculate_penalties(tempBoard):
    """
    Calculates penalty scores based on isolated blocks and holes.
    """
    penalty = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if tempBoard[r][c] == 1:
                emptySpace = 0
                for dir in ADJACENT_DIRECTIONS:
                    nr, nc = dir[0] + r, dir[1] + c
                    if (
                        nr not in range(BOARD_SIZE)
                        or nc not in range(BOARD_SIZE)
                        or tempBoard[nr][nc] == 0
                    ):
                        emptySpace += 1
                if emptySpace > 3:
                    penalty -= emptySpace * ISOLATION_PENALTY_COEFF

    # Penalize Holes
    holes = count_holes(np.copy(tempBoard))
    for hole in holes:
        penalty -= (len(holes) - 1) * 1 / hole * HOLE_PENALTY_COEFF
    return penalty, tempBoard


def evaluate_move(board, shape, row_idx, col_idx):
    """
    Evaluates a potential move by calculating its score and resulting board state.
    """
    tempBoard = np.copy(board)
    score = 0

    # Placing shape
    for block in shape.segment:
        tempBoard[row_idx + block.row][col_idx + block.col] = 1

    # Checking if the computed block's border is touching the border of the board.
    # Adding points to the score if the shape is touching other blocks
    for block in shape.borders:
        if row_idx + block.row not in range(
            BOARD_SIZE
        ) or col_idx + block.col not in range(BOARD_SIZE):
            score += 1
        else:
            score += tempBoard[row_idx + block.row][col_idx + block.col]

    # Finding Completed Columns and Rows and rewarding bonus points
    rows, columns = [], []
    for r in range(BOARD_SIZE):
        if sum(tempBoard[r][c] for c in range(BOARD_SIZE)) == BOARD_SIZE:
            score += BONUS_POINTS
            rows.append(r)

    for c in range(BOARD_SIZE):
        if sum(tempBoard[r][c] for r in range(BOARD_SIZE)) == BOARD_SIZE:
            score += BONUS_POINTS
            columns.append(c)

    # Clearing Completed Rows and Columns in the Board
    for c in columns:
        for r in range(BOARD_SIZE):
            tempBoard[r][c] = 0
    for r in rows:
        for c in range(BOARD_SIZE):
            tempBoard[r][c] = 0
    # Board is now in state after piece is placed and completed row and column are removed

    penalty, tempBoard = calculate_penalties(tempBoard)
    score += penalty
    return score, tempBoard


def solve_board(board, shapes):
    """
    Attempts to solve the board by sequentially placing three shape objects.

    For each permutation of the three shapes, we track every valid placement sequence and game state. At each step:
      - It checks whether the current shape can be placed on the board.
      - Valid placements are evaluated via a scoring system that accounts for border contacts,
        completed rows/columns (with bonus points), and penalties for isolated blocks and holes.
      - Valid moves propagate through successive board states, updating the cumulative score.

    For each valid placement for a given permutation, the resulting board state (i.e.,
    the GameTurn object) is recorded. After exploring all valid permutations, the function selects
    and returns the game state with the highest score.
    """
    originalBoard = np.copy(board)
    completedGames = []
    already_seen = []
    fillCount = np.count_nonzero(board)

    for order in permutations(range(3)):
        if is_permutation_seen(order, already_seen, shapes):
            continue
        already_seen.append(order)

        # Initialize turn for current order
        currentTurn = GameTurn(order)
        currentTurn.board = np.copy(originalBoard)
        boardStates = [currentTurn]  # List of all valid board states
        possible = True

        # Testing each shape in current permuted order
        for shape_idx in order:
            shape = shapes[shape_idx]
            acceptedMoves = (
                []
            )  # Aggregated candidate moves across all board states for the current shape.

            # For each valid board state we must try all order of shape placement (BFS)
            for turn in boardStates:
                validPlacements = (
                    []
                )  # Temporary collection of all valid moves found when trying to place the current shape at different positions on a single board state

                # Loop through all possible positions on the board for the current shape
                for row_idx in range(BOARD_SIZE - shape.height + 1):
                    for col_idx in range(BOARD_SIZE - shape.width + 1):
                        if not try_place_shape(turn.board, shape, row_idx, col_idx):
                            continue

                        # Create new turn with this placement
                        score, tempBoard = evaluate_move(
                            turn.board, shape, row_idx, col_idx
                        )
                        newTurn = GameTurn(
                            order, score + turn.score, np.copy(tempBoard)
                        )
                        newTurn.positions = turn.positions[:]  # shallow copy
                        # Storing positions of shape with score
                        newTurn.positions[shape_idx] = Block(row_idx, col_idx, score)
                        validPlacements.append(newTurn)

                # Done processing the board with all 3 shapes and permutations.
                if len(validPlacements) == 0:
                    # No valid Moves
                    continue

                seenScore = []
                if validPlacements:
                    if fillCount > FILL_COUNT_THRESHOLD:
                        acceptedMoves.extend(validPlacements)
                    else:
                        # Skipping boards(valid placements) with same score because when we have a relatively empty board,
                        # we don't need to consider every valid placement with the same score.
                        seenScore = set()
                        for placement in validPlacements:
                            if placement.score not in seenScore:
                                acceptedMoves.append(placement)
                                seenScore.add(placement.score)

            if len(acceptedMoves) == 0:
                print("impossible")
                possible = False
                break

            # Updating board states with acceptedMoves before next shape
            boardStates = acceptedMoves[:]

        # If possible to place 3 shapes, boardStates will contain a list of GameTurn objects
        # representing all possible ways to place the 3 shapes on the board.
        if possible:
            for turn in boardStates:
                completedGames.append(turn)

    if len(completedGames) > 0:
        completedGames.sort(reverse=True, key=sort_turns)
        print(f"{len(completedGames)} possible boards")
        return completedGames[0]
    else:
        return "Lost"


def generate_step_boards(board, shapes, winning_turn):
    """
    Generates a sequence of board states showing the step-by-step solution.
    """
    step_boards = []
    completion_counter = {1: [], 2: [], 3: []}
    current_board = np.copy(board)
    for step, shape_idx in enumerate(
        winning_turn.order, 1
    ):  # start=1 to use 1,2,3 as markers
        step_board = np.copy(current_board)
        position = winning_turn.positions[shape_idx]

        for block in shapes[shape_idx].segment:
            step_board[position.row + block.row][position.col + block.col] = step + 1

        step_boards.append(step_board)
        current_board = np.copy(step_board)

        completed_rows = 0
        completed_columns = 0
        rows, columns = [], []
        for r in range(BOARD_SIZE):
            if (
                sum(bool(current_board[r][c]) for c in range(BOARD_SIZE)) == BOARD_SIZE
            ):  # using bool() to count any non-zero value
                rows.append(r)
                completed_rows += 1
        for c in range(BOARD_SIZE):
            if sum(bool(current_board[r][c]) for r in range(BOARD_SIZE)) == BOARD_SIZE:
                columns.append(c)
                completed_columns += 1
        completion_counter[step].append([completed_rows, completed_columns])
        for c in columns:
            for r in range(BOARD_SIZE):
                current_board[r][c] = 0
        for r in rows:
            for c in range(BOARD_SIZE):
                current_board[r][c] = 0
    return completion_counter, step_boards

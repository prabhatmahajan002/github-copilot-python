import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def _get_candidates(board, row, col):
    return {
        candidate
        for candidate in range(1, SIZE + 1)
        if is_safe(board, row, col, candidate)
    }

def _find_empty_cell_with_fewest_candidates(board):
    best_cell = None
    best_candidates = None

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                candidates = _get_candidates(board, row, col)
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates
                    if not candidates:
                        return best_cell, best_candidates

    return best_cell, best_candidates

def _count_solutions(board, limit):
    cell, candidates = _find_empty_cell_with_fewest_candidates(board)
    if cell is None:
        return 1
    if not candidates:
        return 0

    row, col = cell
    solution_count = 0
    for candidate in candidates:
        board[row][col] = candidate
        solution_count += _count_solutions(board, limit)
        board[row][col] = EMPTY
        if solution_count >= limit:
            return limit

    return solution_count

def _has_valid_values(board):
    values = set(range(1, SIZE + 1)) | {EMPTY}

    if len(board) != SIZE or any(len(row) != SIZE for row in board):
        return False
    if any(cell not in values for row in board for cell in row):
        return False

    for row in board:
        filled = [cell for cell in row if cell != EMPTY]
        if len(filled) != len(set(filled)):
            return False

    for col in range(SIZE):
        filled = [board[row][col] for row in range(SIZE) if board[row][col] != EMPTY]
        if len(filled) != len(set(filled)):
            return False

    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            filled = [
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
                if board[row][col] != EMPTY
            ]
            if len(filled) != len(set(filled)):
                return False

    return True

def count_solutions(board, limit=2):
    if limit < 1:
        raise ValueError('limit must be at least 1')
    if not _has_valid_values(board):
        return 0
    return _count_solutions(deep_copy(board), limit)

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board, clues):
    if clues < 0 or clues > SIZE * SIZE:
        raise ValueError('clues must be between 0 and 81')

    current_clues = sum(cell != EMPTY for row in board for cell in row)
    if current_clues < clues:
        raise ValueError('clues cannot exceed the current number of filled cells')

    positions = [
        (row, col)
        for row in range(SIZE)
        for col in range(SIZE)
        if board[row][col] != EMPTY
    ]
    random.shuffle(positions)

    for row, col in positions:
        if current_clues == clues:
            return

        original_value = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board) == 1:
            current_clues -= 1
        else:
            board[row][col] = original_value

    if current_clues != clues:
        raise ValueError('could not create a unique puzzle with the requested clues')

def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution

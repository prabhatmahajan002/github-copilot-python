import sudoku_logic


def start_new_game(game_state, clues=35):
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    game_state['puzzle'] = puzzle
    game_state['solution'] = solution
    return puzzle


def find_incorrect_cells(board, solution):
    incorrect = []
    for row in range(sudoku_logic.SIZE):
        for column in range(sudoku_logic.SIZE):
            if board[row][column] != solution[row][column]:
                incorrect.append([row, column])
    return incorrect
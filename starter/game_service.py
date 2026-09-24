import sudoku_logic


DIFFICULTY_LEVELS = {
    'easy': 45,
    'medium': 35,
    'hard': 27,
}


def get_clues_for_difficulty(difficulty='medium', clues=None):
    if clues is not None:
        clue_count = int(clues)
        if clue_count < 0 or clue_count > sudoku_logic.SIZE * sudoku_logic.SIZE:
            raise ValueError('clues must be between 0 and 81')
        return clue_count

    if difficulty is None:
        difficulty_name = 'medium'
    else:
        difficulty_name = str(difficulty).strip().lower()

    if not difficulty_name:
        difficulty_name = 'medium'

    if difficulty_name not in DIFFICULTY_LEVELS:
        raise ValueError('Invalid difficulty. Supported values: easy, medium, hard.')

    return DIFFICULTY_LEVELS[difficulty_name]


def start_new_game(game_state, difficulty='medium', clues=None):
    if clues is None and isinstance(difficulty, int):
        clues = difficulty
        difficulty = 'medium'

    clue_count = get_clues_for_difficulty(difficulty=difficulty, clues=clues)
    puzzle, solution = sudoku_logic.generate_puzzle(clue_count)
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
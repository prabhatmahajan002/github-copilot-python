import pytest
import sudoku_logic


def assert_valid_solution(board):
    expected_values = set(range(1, sudoku_logic.SIZE + 1))

    for row in board:
        assert set(row) == expected_values

    for column in range(sudoku_logic.SIZE):
        assert {board[row][column] for row in range(sudoku_logic.SIZE)} == expected_values

    for start_row in range(0, sudoku_logic.SIZE, 3):
        for start_column in range(0, sudoku_logic.SIZE, 3):
            box = {
                board[row][column]
                for row in range(start_row, start_row + 3)
                for column in range(start_column, start_column + 3)
            }
            assert box == expected_values


def test_create_empty_board_returns_nine_by_nine_empty_board():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_does_not_modify_original_board():
    original = [[1, 2], [3, 4]]

    copied = sudoku_logic.deep_copy(original)
    copied[0][0] = 9

    assert original == [[1, 2], [3, 4]]
    assert copied == [[9, 2], [3, 4]]


def test_is_safe_rejects_values_already_used_in_row_column_or_box():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[1][1] = 2
    board[3][3] = 3

    assert not sudoku_logic.is_safe(board, 0, 1, 1)
    assert not sudoku_logic.is_safe(board, 2, 1, 2)
    assert not sudoku_logic.is_safe(board, 2, 2, 1)
    assert sudoku_logic.is_safe(board, 0, 1, 3)


def test_fill_board_creates_a_complete_valid_solution():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board)
    assert_valid_solution(board)


def test_count_solutions_returns_one_for_a_valid_completed_board():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(board)

    assert sudoku_logic.count_solutions(board) == 1


def test_count_solutions_returns_zero_for_an_invalid_board():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert sudoku_logic.count_solutions(board) == 0


def test_count_solutions_detects_multiple_solutions():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(board) == 2


def test_count_solutions_does_not_modify_input_board():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    original = sudoku_logic.deep_copy(board)

    sudoku_logic.count_solutions(board)

    assert board == original


def test_remove_cells_leaves_requested_number_of_clues():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(board)

    sudoku_logic.remove_cells(board, clues=35)

    assert sum(cell != sudoku_logic.EMPTY for row in board for cell in row) == 35


def test_remove_cells_rejects_invalid_clue_counts():
    board = sudoku_logic.create_empty_board()

    with pytest.raises(ValueError):
        sudoku_logic.remove_cells(board, clues=-1)
    with pytest.raises(ValueError):
        sudoku_logic.remove_cells(board, clues=82)


def test_generate_puzzle_rejects_invalid_clue_counts():
    with pytest.raises(ValueError):
        sudoku_logic.generate_puzzle(clues=-1)
    with pytest.raises(ValueError):
        sudoku_logic.generate_puzzle(clues=82)


def test_generate_puzzle_returns_solution_and_matching_prefilled_cells():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert_valid_solution(solution)
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    for row in range(sudoku_logic.SIZE):
        for column in range(sudoku_logic.SIZE):
            if puzzle[row][column] != sudoku_logic.EMPTY:
                assert puzzle[row][column] == solution[row][column]


def test_generate_puzzle_has_exactly_one_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle) == 1
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    for row in range(sudoku_logic.SIZE):
        for column in range(sudoku_logic.SIZE):
            if puzzle[row][column] != sudoku_logic.EMPTY:
                assert puzzle[row][column] == solution[row][column]
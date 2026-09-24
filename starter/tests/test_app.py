import app
import sudoku_logic


def test_index_returns_the_game_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_returns_puzzle_and_stores_current_game(client):
    response = client.get('/new?difficulty=medium')

    assert response.status_code == 200
    data = response.get_json()
    puzzle = data['puzzle']
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert puzzle == app.CURRENT['puzzle']
    assert app.CURRENT['solution'] is not None


def test_new_generates_requested_difficulty_levels(client):
    for difficulty, expected_clues in [('easy', 45), ('medium', 35), ('hard', 27)]:
        response = client.get(f'/new?difficulty={difficulty}')

        assert response.status_code == 200
        puzzle = response.get_json()['puzzle']
        clues = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)
        assert clues == expected_clues
        assert sudoku_logic.count_solutions(puzzle) == 1


def test_new_defaults_to_medium_when_difficulty_is_omitted(client):
    response = client.get('/new')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    clues = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)
    assert clues == 35


def test_new_supports_case_insensitive_difficulty_names(client):
    response = client.get('/new?difficulty=HARd')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    clues = sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)
    assert clues == 27


def test_new_rejects_invalid_difficulty_values(client):
    response = client.get('/new?difficulty=expert')

    assert response.status_code == 400
    assert response.get_json() == {
        'error': 'Invalid difficulty. Supported values: easy, medium, hard.'
    }


def test_check_returns_error_when_no_game_is_in_progress(client):
    response = client.post('/check', json={'board': sudoku_logic.create_empty_board()})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_identifies_incorrect_cells(client):
    client.get('/new')
    board = sudoku_logic.deep_copy(app.CURRENT['solution'])
    board[0][0] = (board[0][0] % sudoku_logic.SIZE) + 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert [0, 0] in response.get_json()['incorrect']


def test_check_returns_no_incorrect_cells_for_the_current_solution(client):
    client.get('/new')
    board = sudoku_logic.deep_copy(app.CURRENT['solution'])

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}
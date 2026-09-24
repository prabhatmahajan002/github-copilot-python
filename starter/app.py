from flask import Flask, render_template, jsonify, request
import game_service

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    clues = request.args.get('clues')

    try:
        if difficulty is not None and difficulty.strip() != '':
            puzzle = game_service.start_new_game(CURRENT, difficulty=difficulty)
        elif clues is not None and clues.strip() != '':
            puzzle = game_service.start_new_game(CURRENT, clues=int(clues))
        else:
            puzzle = game_service.start_new_game(CURRENT, difficulty='medium')
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    return jsonify({'puzzle': puzzle})


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if not _is_valid_board(board):
        return jsonify({'error': 'Invalid board'}), 400

    incorrect = game_service.find_incorrect_cells(board, solution)
    return jsonify({'incorrect': incorrect})


@app.route('/hint', methods=['POST'])
def get_hint():
    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if not _is_valid_board(board):
        return jsonify({'error': 'Invalid board'}), 400

    for row in range(9):
        for column in range(9):
            if puzzle[row][column] == 0 and board[row][column] == 0:
                return jsonify({
                    'row': row,
                    'column': column,
                    'value': solution[row][column],
                })

    return jsonify({'hint': None, 'message': 'No empty cells available for a hint.'})


def _is_valid_board(board):
    if not isinstance(board, list) or len(board) != 9:
        return False
    if any(not isinstance(row, list) or len(row) != 9 for row in board):
        return False
    return all(
        isinstance(cell, int) and not isinstance(cell, bool) and 0 <= cell <= 9
        for row in board
        for cell in row
    )


if __name__ == '__main__':
    app.run(debug=True)
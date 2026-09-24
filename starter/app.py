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
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = game_service.find_incorrect_cells(board, solution)
    return jsonify({'incorrect': incorrect})


if __name__ == '__main__':
    app.run(debug=True)
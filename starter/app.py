from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

DIFFICULTY_CLUES = {
    'Easy': 45,
    'Medium': 35,
    'Hard': 25,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    clues = DIFFICULTY_CLUES.get(difficulty, int(request.args.get('clues', 35)))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})


@app.route('/hint', methods=['POST'])
def give_hint():
    data = request.json or {}
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'Invalid board'}), 400

    for row in range(sudoku_logic.SIZE):
        if not isinstance(board[row], list) or len(board[row]) != sudoku_logic.SIZE:
            return jsonify({'error': 'Invalid board'}), 400
        for col in range(sudoku_logic.SIZE):
            if board[row][col] in (0, None, ''):
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': solution[row][col],
                })

    return jsonify({'row': None, 'col': None, 'value': None})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid request'}), 400

    board = data.get('board')
    solution = CURRENT.get('solution')

    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    # Validate the submitted board before comparing it
    if not sudoku_logic.is_valid_solution(board):
        return jsonify({
            'error': 'Invalid Sudoku solution'
        }), 400

    incorrect = []

    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])

    return jsonify({'incorrect': incorrect})
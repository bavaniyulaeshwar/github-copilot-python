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

# Copilot suggested adding extra validation for board dimensions,
# row/column types, and 3x3 box values. I critically reviewed
# the suggestion and adapted it to this project's existing SIZE
# constant and Sudoku structure. I kept the useful validation
# checks while avoiding changes to the existing solving behavior.

def is_valid_solution(board):
    expected = set(range(1, SIZE + 1))

    if not isinstance(board, list) or len(board) != SIZE:
        return False

    if any(
        not isinstance(row, list)
        or len(row) != SIZE
        or any(type(value) is not int or value not in expected for value in row)
        for row in board
    ):
        return False

    if any(set(row) != expected for row in board):
        return False

    if any(
        {board[row][col] for row in range(SIZE)} != expected
        for col in range(SIZE)
    ):
        return False

    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            box = {
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            }
            if box != expected:
                return False

    return True

def count_solutions(board, limit=2):
    solutions = 0

    def search():
        nonlocal solutions
        if solutions >= limit:
            return

        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    for candidate in range(1, SIZE + 1):
                        if is_safe(board, row, col, candidate):
                            board[row][col] = candidate
                            search()
                            board[row][col] = EMPTY
                    return

        solutions += 1

    search()
    return solutions


def has_unique_solution(board):
    return count_solutions(board, limit=2) == 1


def remove_cells(board, clues):
    if not 0 <= clues <= SIZE * SIZE:
        raise ValueError("clues must be between 0 and 81")

    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    target_removals = SIZE * SIZE - clues

    def try_remove(index, removed):
        if removed == target_removals:
            return True

        if len(positions) - index < target_removals - removed:
            return False

        for pos in range(index, len(positions)):
            row, col = positions[pos]

            if board[row][col] == EMPTY:
                continue

            value = board[row][col]
            board[row][col] = EMPTY

            if has_unique_solution(board):
                if try_remove(pos + 1, removed + 1):
                    return True

            board[row][col] = value

        return False

    if not try_remove(0, 0):
        raise ValueError(
            "could not generate a uniquely solvable puzzle with this clue count"
        )
    
def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution

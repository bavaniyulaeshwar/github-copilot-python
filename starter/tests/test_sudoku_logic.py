import sudoku_logic


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_does_not_modify_original_board():
    board = sudoku_logic.create_empty_board()
    copied_board = sudoku_logic.deep_copy(board)
    copied_board[0][0] = 1

    assert board[0][0] == sudoku_logic.EMPTY


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 5
    board[1][0] = 6
    board[1][1] = 7

    assert not sudoku_logic.is_safe(board, 0, 0, 5)
    assert not sudoku_logic.is_safe(board, 0, 0, 6)
    assert not sudoku_logic.is_safe(board, 0, 0, 7)
    assert sudoku_logic.is_safe(board, 0, 0, 1)


def test_fill_board_creates_a_complete_valid_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board)
    assert all(cell in range(1, sudoku_logic.SIZE + 1) for row in board for cell in row)

    for index in range(sudoku_logic.SIZE):
        assert set(board[index]) == set(range(1, sudoku_logic.SIZE + 1))
        assert {board[row][index] for row in range(sudoku_logic.SIZE)} == set(
            range(1, sudoku_logic.SIZE + 1)
        )


def test_count_solutions_stops_after_two_solutions():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(board) == 2


def test_has_unique_solution_distinguishes_unique_and_non_unique_boards():
    solved_board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(solved_board)

    assert sudoku_logic.has_unique_solution(solved_board)
    assert not sudoku_logic.has_unique_solution(sudoku_logic.create_empty_board())


def test_generate_puzzle_removes_requested_cells_and_preserves_solution():
    clues = 35

    puzzle, solution = sudoku_logic.generate_puzzle(clues)

    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == clues
    assert all(
        puzzle[row][col] in (sudoku_logic.EMPTY, solution[row][col])
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )
    assert all(
        cell in range(1, sudoku_logic.SIZE + 1)
        for row in solution
        for cell in row
    )
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_generated_puzzles_have_exactly_one_solution():
    for _ in range(3):
        puzzle, _ = sudoku_logic.generate_puzzle(35)

        assert sudoku_logic.count_solutions(puzzle) == 1
# Sudoku Project Instructions

## Project Overview
This project is a Flask-based Sudoku game. Keep the application
modular, readable, maintainable, and easy to understand.

## Coding Standards
- Use clear Python functions and meaningful variable names.
- Keep Sudoku logic separate from Flask routes and UI code.
- Avoid unnecessary duplication.
- Add comments where the logic is not obvious.
- Handle invalid input safely.
- Preserve existing working functionality when making changes.

## Sudoku Requirements
- Generate valid Sudoku puzzles.
- Every generated puzzle must have exactly one unique solution.
- Support Easy, Medium, and Hard difficulty levels.
- Prefilled cells must remain locked.
- Detect invalid user entries and provide immediate feedback.
- Display a completion message when the puzzle is solved correctly.

## Game Features
- Provide a Hint button that fills one correct empty cell and locks it.
- Provide a Check button that identifies incorrect entries.
- Include a timer.
- Include a dark/light mode toggle.
- Maintain a Top 10 scoreboard using browser localStorage.
- Store player name, completion time, difficulty, and hints used.

## UI Requirements
- Use responsive HTML/CSS.
- Make the Sudoku grid readable on desktop and mobile.
- Use alternating styling for the 3x3 Sudoku squares.
- Ensure text and controls remain readable in both light and dark modes.

## Testing
- Preserve all existing tests.
- Run the test suite after significant changes.
- Do not remove tests simply to make them pass.
- When adding important functionality, add appropriate tests where practical.

## Copilot Usage
When suggesting code changes:
1. Explain what the change does.
2. Preserve existing functionality.
3. Prefer small, understandable changes.
4. Evaluate suggestions before accepting them.
5. Do not introduce unnecessary dependencies.
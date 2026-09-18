// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let gameStartedAt = null;
let hintsUsed = 0;
let gameCompleted = false;

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      const boxTone = (Math.floor(i / 3) + Math.floor(j / 3)) % 2 === 0
        ? 'box-tone-a'
        : 'box-tone-b';
      input.className = `sudoku-cell ${boxTone}`;
      input.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}`);
      input.setAttribute('role', 'gridcell');
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const res = await fetch('/new');
  const data = await res.json();
  renderPuzzle(data.puzzle);
  gameStartedAt = Date.now();
  hintsUsed = 0;
  gameCompleted = false;
  document.getElementById('message').innerText = '';
}

function renderLeaderboard() {
  const list = document.getElementById('leaderboard-list');
  list.innerHTML = '';
  SudokuLeaderboard.getScores(window.localStorage).forEach((score) => {
    const item = document.createElement('li');
    item.textContent = `${score.name} - ${score.completionTime}s - ${score.difficulty} - ${score.hintsUsed} hints`;
    list.appendChild(item);
  });
}

function saveCompletedGame() {
  const name = window.prompt('Enter your name for the leaderboard:', 'Anonymous');
  SudokuLeaderboard.addScore(window.localStorage, {
    name,
    completionTime: Math.floor((Date.now() - gameStartedAt) / 1000),
    difficulty: document.getElementById('difficulty').value,
    hintsUsed
  });
  renderLeaderboard();
}

async function checkSolution() {
  if (gameCompleted) return;

  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    gameCompleted = true;
    msg.style.color = 'var(--message-success)';
    msg.innerText = 'Congratulations! You solved it!';
    saveCompletedGame();
  } else {
    msg.style.color = 'var(--message-error)';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  renderLeaderboard();
  // initialize
  newGame();
});
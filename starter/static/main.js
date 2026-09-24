// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerInterval = null;
let gameCompleted = false;
let gameDifficulty = 'medium';

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainingSeconds = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainingSeconds}`;
}

function updateTimerDisplay() {
  document.getElementById('timer').innerText = formatTime(elapsedSeconds);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function resetGameState(difficulty) {
  stopTimer();
  hintsUsed = 0;
  elapsedSeconds = 0;
  gameCompleted = false;
  gameDifficulty = difficulty;
  updateTimerDisplay();
  document.getElementById('hints-used').innerText = 'Hints used: 0';
}

function setMessage(text, color = '#d32f2f') {
  const message = document.getElementById('message');
  message.style.color = color;
  message.innerText = text;
}

function isBoardComplete(board) {
  return board.every((row) => row.every((value) => value >= 1 && value <= 9));
}

function completeGame() {
  if (gameCompleted) return;
  gameCompleted = true;
  stopTimer();
  setMessage(
    `Congratulations! Completed in ${formatTime(elapsedSeconds)}. ` +
    `Difficulty: ${gameDifficulty}. Hints used: ${hintsUsed}.`,
    '#388e3c'
  );
}

function getBoardInputs() {
  return document.querySelectorAll('#sudoku-board input');
}

function readBoard() {
  const board = [];
  const inputs = getBoardInputs();
  for (let row = 0; row < SIZE; row++) {
    board[row] = [];
    for (let col = 0; col < SIZE; col++) {
      const input = inputs[row * SIZE + col];
      board[row][col] = input.value ? parseInt(input.value, 10) : 0;
    }
  }
  return board;
}

function validateInput(value) {
  const sanitized = value.replace(/[^1-9]/g, '').slice(0, 1);
  return {
    value: sanitized,
    isValid: value === sanitized,
  };
}

function findConflicts(board) {
  const conflicts = new Set();
  const inspectUnit = (cells) => {
    const seen = new Map();
    cells.forEach(([row, col]) => {
      const value = board[row][col];
      if (!value) return;
      if (!seen.has(value)) seen.set(value, []);
      seen.get(value).push(row * SIZE + col);
    });
    seen.forEach((indexes) => {
      if (indexes.length > 1) indexes.forEach((index) => conflicts.add(index));
    });
  };

  for (let index = 0; index < SIZE; index++) {
    inspectUnit(Array.from({length: SIZE}, (_, offset) => [index, offset]));
    inspectUnit(Array.from({length: SIZE}, (_, offset) => [offset, index]));
  }
  for (let boxRow = 0; boxRow < SIZE; boxRow += 3) {
    for (let boxCol = 0; boxCol < SIZE; boxCol += 3) {
      inspectUnit(
        Array.from({length: 9}, (_, offset) => [
          boxRow + Math.floor(offset / 3),
          boxCol + (offset % 3),
        ])
      );
    }
  }
  return conflicts;
}

function applyInvalidStyling(conflicts) {
  getBoardInputs().forEach((input, index) => {
    if (!input.disabled) input.classList.toggle('invalid', conflicts.has(index));
  });
}

function clearIncorrectStyling() {
  getBoardInputs().forEach((input) => input.classList.remove('incorrect'));
}

function handleBoardInput(event) {
  const input = event.target;
  if (!(input instanceof HTMLInputElement) || input.disabled) return;

  const validation = validateInput(input.value);
  input.value = validation.value;
  applyInvalidStyling(findConflicts(readBoard()));
  const conflicts = findConflicts(readBoard());
  input.classList.toggle('invalid', !validation.isValid || conflicts.has(Number(input.dataset.row) * SIZE + Number(input.dataset.col)));
  if (conflicts.size > 0 || !validation.isValid) {
    setMessage('Invalid move.');
  } else if (document.getElementById('message').innerText === 'Invalid move.') {
    setMessage('', '#333');
  }
  evaluateCompletion();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  boardDiv.oninput = handleBoardInput;
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.inputMode = 'numeric';
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
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
        inp.readOnly = true;
        inp.className = 'sudoku-cell prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.readOnly = false;
        inp.className = 'sudoku-cell';
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const query = new URLSearchParams({difficulty}).toString();
  resetGameState(difficulty);
  try {
    const res = await fetch(`/new?${query}`);
    const data = await res.json();

    if (!res.ok) {
      setMessage(data.error || 'Unable to start a new game.');
      return;
    }

    renderPuzzle(data.puzzle);
    setMessage('', '#333');
    startTimer();
  } catch (error) {
    setMessage('Unable to connect to the game server.');
  }
}

async function requestHint() {
  if (gameCompleted) return;
  try {
    const res = await fetch('/hint', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board: readBoard()})
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      setMessage(data.error || 'Unable to get a hint.');
      return;
    }
    if (data.hint === null) {
      setMessage(data.message || 'No empty cells available for a hint.');
      return;
    }

    const input = getBoardInputs()[data.row * SIZE + data.column];
    input.value = data.value;
    input.disabled = true;
    input.readOnly = true;
    input.className = 'sudoku-cell hinted';
    hintsUsed += 1;
    document.getElementById('hints-used').innerText = `Hints used: ${hintsUsed}`;
    setMessage(`Hint used: ${hintsUsed}.`, '#795548');
    evaluateCompletion();
  } catch (error) {
    setMessage('Unable to connect to the game server.');
  }
}

async function evaluateCompletion() {
  if (gameCompleted || !isBoardComplete(readBoard())) return;
  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board: readBoard()})
    });
    const data = await res.json();
    if (res.ok && !data.error && data.incorrect.length === 0) completeGame();
  } catch (error) {
    setMessage('Unable to verify puzzle completion.');
  }
}

async function checkPuzzle() {
  clearIncorrectStyling();
  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board: readBoard()})
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      setMessage(data.error || 'Unable to check the puzzle.');
      return;
    }

    const incorrect = new Set(data.incorrect.map(([row, col]) => row * SIZE + col));
    getBoardInputs().forEach((input, index) => {
      if (!input.disabled && incorrect.has(index)) input.classList.add('incorrect');
    });
    if (incorrect.size === 0 && isBoardComplete(readBoard())) {
      completeGame();
    } else if (incorrect.size === 0) {
      setMessage('All entered cells are correct.', '#388e3c');
    } else {
      setMessage('Some cells are incorrect.');
    }
  } catch (error) {
    setMessage('Unable to connect to the game server.');
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkPuzzle);
  // initialize
  newGame();
});
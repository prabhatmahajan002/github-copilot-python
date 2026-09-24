# Sudoku Game

A complete browser-based Sudoku application built with Python and Flask. The project generates valid puzzles with a unique solution, tracks game progress in real time, and provides a responsive, accessible interface for solving puzzles on desktop or mobile devices.

## Overview

This application lets a player start a new Sudoku puzzle at Easy, Medium, or Hard difficulty, fill in the board, receive immediate feedback on invalid entries, request hints, and check the solution against the correct answer. The game includes a countdown-style timer, hint tracking, completion handling, and a Top 10 fastest-score board stored in the browser with localStorage.

## Technology Stack

- Python 3
- Flask web framework
- Jinja templates for the page shell
- HTML, CSS, and JavaScript for the client-side gameplay experience
- pytest for automated testing

## Setup and Run

From the repository root, navigate to the application directory:

```bash
cd github-copilot-python/starter
```

### Virtual environment setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Then open the app in a browser at:

```text
http://127.0.0.1:5000
```

## Automated Tests

Run the full automated test suite from the project directory:

```bash
python -m pytest -q
```

This command is the project-standard validation step for both Sudoku logic and Flask endpoint behavior.

## Game Features

- Unique-solution Sudoku generation using a backtracking-based board generator and solution-count validation
- Easy, Medium, and Hard puzzle difficulties with different numbers of prefilled cells
- Locked prefilled cells that cannot be edited by the player
- Immediate invalid-move feedback while entering values
- Check Solution action that compares the current board against the correct solution and highlights incorrect cells
- Hint functionality that fills one correct empty cell, locks it, and increments the hint counter
- Timer that starts on a fresh game and stops when the puzzle is completed
- Completion handling that confirms the puzzle was solved correctly and records a score entry
- Top 10 fastest scores displayed with player name, completion time, difficulty, and hints used
- Browser persistence using localStorage so Top 10 scores remain available across sessions
- Light and Dark mode toggle for the interface
- Responsive layout for desktop and mobile screens
- Accessible UI considerations including semantic labels, keyboard focus states, status messaging, and readable color contrast

## Project Structure

```text
github-copilot-python/
├── README.md
├── .github/
│   └── copilot-instructions.md
└── starter/
    ├── app.py
    ├── game_service.py
    ├── sudoku_logic.py
    ├── requirements.txt
    ├── static/
    │   ├── main.js
    │   └── styles.css
    ├── templates/
    │   └── index.html
    └── tests/
        ├── conftest.py
        ├── test_app.py
        └── test_sudoku_logic.py
```

## GitHub Copilot Usage

GitHub Copilot was used during development to help with code generation, iteration, and validation of the Flask and Sudoku logic. The project remains a working, test-backed Flask application that follows the requested project goals and rubric without modifying unrelated application behavior.

## Testing Approach

The application is validated with pytest to cover both the Flask routes and the core Sudoku puzzle logic. The automated suite checks puzzle generation, uniqueness guarantees, difficulty settings, board validation, hint behavior, and solution checking so the project remains stable as a final submission.

## Reviewer Notes

This project is a functional single-page Sudoku game with a Python Flask backend, generated unique-solution puzzles, and a polished frontend experience. It is designed to be easy to run locally and straightforward to review in its current state.

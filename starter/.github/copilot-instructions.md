# GitHub Copilot Instructions - Flask Sudoku Project

## Project Goal

This project refactors a legacy Python Flask Sudoku application into a
modern, maintainable, responsive application while preserving existing
functionality and satisfying the Udacity project rubric.

## General Development Guidelines

- Write readable, maintainable, and modular code.
- Use descriptive variable, function, class, and file names.
- Keep functions focused on a single responsibility.
- Avoid duplicated logic.
- Prefer simple solutions over unnecessary complexity.
- Preserve working existing functionality during refactoring.
- Do not modify unrelated code when implementing a feature.
- Explain significant architectural or technical changes before making them.
- Handle expected errors gracefully and consistently.
- Add comments only where they improve understanding of non-obvious logic.

## Python and Flask

- Follow modern Python conventions and PEP 8.
- Separate Sudoku game logic from Flask routing where practical.
- Use reusable functions and modules.
- Use type hints where they improve clarity.
- Avoid unnecessary global state.
- Keep Flask routes focused on HTTP request and response handling.
- Validate data received by backend endpoints.

## Sudoku Requirements

- Generated Sudoku puzzles must have exactly one unique solution.
- Support Easy, Medium, and Hard difficulty levels.
- Difficulty must affect the number of prefilled cells.
- Prefilled cells must be locked and not editable.
- Invalid user moves must receive immediate visual feedback.
- The Check feature must identify incorrect user entries.
- The Hint feature must fill one correct empty cell and lock that cell.
- Track the number of hints used.
- Correctly solving a puzzle must trigger a completion message.

## Timer and Scores

- Start or reset the timer when a new game begins.
- Stop the timer when the puzzle is completed successfully.
- Maintain a Top 10 fastest-times scoreboard.
- Score entries must contain player name, completion time, difficulty,
  and number of hints used.
- Store Top 10 score data in browser localStorage so it persists across sessions.
- Keep only the appropriate Top 10 entries after scores are updated.

## Frontend JavaScript

- Keep JavaScript functions small and focused.
- Prefer event delegation where appropriate.
- Keep game state management understandable and predictable.
- Avoid unnecessary inline JavaScript.
- Validate user input and provide clear visual feedback.

## Styling and Accessibility

- Support both light and dark modes across the entire interface.
- Ensure text, controls, borders, and game cells remain readable in both modes.
- Make the interface responsive for desktop and mobile screen sizes.
- Visually distinguish alternating 3x3 Sudoku regions.
- Avoid layout shifts when Sudoku region colors or states change.
- Use accessible labels and semantic HTML where practical.
- Maintain clear keyboard focus states and sufficient visual contrast.

## Testing

- Establish a working automated testing baseline before refactoring
  application code.
- Do not refactor existing application logic until baseline tests pass.
- Preserve existing tests when adding features unless a requirement
  legitimately changes expected behavior.
- Add tests for important Sudoku logic and feature behavior where practical.
- Run the complete test suite after each major refactor or feature.
- Clearly explain failing tests rather than changing tests merely to make
  failures disappear.

## Working With Copilot

- Explain proposed significant

GitHub Copilot Instructions - Flask Sudoku Project
Project Goal
This project refactors a legacy Python Flask Sudoku application into a modern, maintainable, responsive application while preserving existing functionality and satisfying the Udacity project rubric.

General Development Guidelines
Write readable, maintainable, and modular code.
Use descriptive variable, function, class, and file names.
Keep functions focused on a single responsibility.
Avoid duplicated logic.
Prefer simple solutions over unnecessary complexity.
Preserve working existing functionality during refactoring.
Do not modify unrelated code when implementing a feature.
Explain significant architectural or technical changes before making them.
Handle expected errors gracefully and consistently.
Add comments only where they improve understanding of non-obvious logic.
Python and Flask
Follow modern Python conventions and PEP 8.
Separate Sudoku game logic from Flask routing where practical.
Use reusable functions and modules.
Use type hints where they improve clarity.
Avoid unnecessary global state.
Keep Flask routes focused on HTTP request and response handling.
Validate data received by backend endpoints.
Sudoku Requirements
Generated Sudoku puzzles must have exactly one unique solution.
Support Easy, Medium, and Hard difficulty levels.
Difficulty must affect the number of prefilled cells.
Prefilled cells must be locked and not editable.
Invalid user moves must receive immediate visual feedback.
The Check feature must identify incorrect user entries.
The Hint feature must fill one correct empty cell and lock that cell.
Track the number of hints used.
Correctly solving a puzzle must trigger a completion message.
Timer and Scores
Start or reset the timer when a new game begins.
Stop the timer when the puzzle is completed successfully.
Maintain a Top 10 fastest-times scoreboard.
Score entries must contain player name, completion time, difficulty, and number of hints used.
Store Top 10 score data in browser localStorage so it persists across sessions.
Keep only the appropriate Top 10 entries after scores are updated.
Frontend JavaScript
Keep JavaScript functions small and focused.
Prefer event delegation where appropriate.
Keep game state management understandable and predictable.
Avoid unnecessary inline JavaScript.
Validate user input and provide clear visual feedback.
Styling and Accessibility
Support both light and dark modes across the entire interface.
Ensure text, controls, borders, and game cells remain readable in both modes.
Make the interface responsive for desktop and mobile screen sizes.
Visually distinguish alternating 3x3 Sudoku regions.
Avoid layout shifts when Sudoku region colors or states change.
Use accessible labels and semantic HTML where practical.
Maintain clear keyboard focus states and sufficient visual contrast.
Testing
Establish a working automated testing baseline before refactoring application code.
Do not refactor existing application logic until baseline tests pass.
Preserve existing tests when adding features unless a requirement legitimately changes expected behavior.
Add tests for important Sudoku logic and feature behavior where practical.
Run the complete test suite after each major refactor or feature.
Clearly explain failing tests rather than changing tests merely to make failures disappear.
Working With Copilot
Explain proposed significant.
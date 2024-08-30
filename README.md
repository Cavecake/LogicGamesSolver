# Sudoku Variant Solver
This repository contains a solver, that can solve any classic sudoku or killer sudoku (a sudoku variant). As long as there is at least one solution.

## Alogrithm
The algorithm is a classic backtracing algorithm.

## Installation
Download the files from the repository
Run `cd /path/to/your/dir`
To start the classic sudoku solver run:
```
python sudokuGUI.py
```
To start the solver for the killer variant run:
```
python killerSudoku.py
```

## How to use the program
### Selection
In both versions of the program you first need to insert the numbers, that are provided by the sudoku.
You can select cells by clicking them with the left mouse button.
To select multiple cells either drag, while holding the left mouse button, or use the shift key with the left mouse button.
To deselect use the right mouse button.

### Numbers
Numbers kann be added using the number keys on your keyboard and removed by using the BACKSPACE or DELETE keys.

### Starting Solver/Moving to next input phase
Now you need to press enter. In case of a normal sudoku the solution will appear.

### Creating cages
To create cages select the cells, that will belong to the cage.
If you try to select cells, that are already contained in a cell, the cage will be added to your selection.
Afterwards you will be required to enter the sum for the cage.
The cage will be stored after you release the shift key. In case it was not pressed during the selection simply press and release the key.

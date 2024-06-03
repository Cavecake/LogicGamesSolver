import sudoku
from sudokuGUI import SudokuGUI
import pyglet
import copy

class KillerSuoku(sudoku.Sudoku):
    def __init__(self, grid, cell_groups) -> None:
        super().__init__(grid)
        self.cell_groups = cell_groups
    def valid_move(self, cell_x, cell_y, number):
        for group in self.cell_groups:
            if not [cell_x, cell_y] in group[1]:
                continue

            summe = 0
            for cell in group[1]:
                if cell == [cell_x, cell_y]:
                    continue
                if self.grid[cell[1]][cell[0]] == number:
                    return False
                summe += self.grid[cell[1]][cell[0]]
            if summe + number > group[0]:
                return False
        return super().valid_move(cell_x, cell_y, number)
    
class KillerSudokuGUI(SudokuGUI):
    def __init__(self) -> None:
        self.cell_groups = []
        self.createBox = False
        self.box_number = ""
        super().__init__()

    def solve(self):
        sud = KillerSuoku(self.grid,self.cell_groups)
        self.solved_grid = sud.dynamicSolver()
        self.solved = True

    def drawSudokuNumbers(self):
        labels = []
        if self.createBox:
            for group in self.cell_groups:
                for cell in group[1]:
                    x, y = cell
                    self.drawLetter(x,8 - y,labels,group[0],self.NUMBER_COLOR, font_size = 14, offset = [0,0])
            
            for cell in self.selectedCells:
                x, y = cell
                self.drawLetter(x,8 - y,labels,self.box_number,self.SOLUTION_COLOR, font_size = 14, offset = [0,0])

        return labels + super().drawSudokuNumbers()

    def on_key_press(self, symbol, modifiers):
        if symbol in [pyglet.window.key.ENTER, pyglet.window.key.RETURN]:
            if self.createBox:
                self.solve()
            else:
                self.createBox = True
        elif self.createBox:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                self.setMutliselect(True)
            if symbol == pyglet.window.key.DELETE or symbol == pyglet.window.key.BACKSPACE:
                self.box_number = self.box_number[:-1]
            number = pyglet.window.key.symbol_string(symbol)
            number = number[-1]
            if number in ["1","2","3","4","5","6","7","8","9"]:
                self.box_number += number
        else:
            return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if not self.createBox: 
            return super().on_key_release(symbol, modifiers)
        
        key = pyglet.window.key.symbol_string(symbol)
        if key[1:] == "SHIFT":
            self.cell_groups.append([int(self.box_number),self.selectedCells.copy()])
            self.box_number = ""
            self.selectedCells = []
            self.setMutliselect(False)

    def selectCell(self, x, y):
        cell = [x,y]
        for group in self.cell_groups:
            if cell in group[1]:
                self.box_number = group[0]
                temp = [cell for cell in group[1] if cell not in self.selectedCells]
                self.selectedCells = self.selectedCells + temp
        return super().selectCell(x, y)

if __name__ == "__main__":
    gui = KillerSudokuGUI()
    gui.start()
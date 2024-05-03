import sudoku
import pyglet
class KillerSuoku(sudoku.Sudoku):
    def __init__(self, grid, cell_groups) -> None:
        super().__init__(grid)
        self.cell_groups = cell_groups
    def valid_move(self, cell_x, cell_y, number):
        for group in self.cell_groups:
            if not [cell_x, cell_y] in group:
                continue

            summe = 0
            for cell in group[1:]:
                if self.grid[cell[1]][cell[0]] == number:
                    return False
                summe += self.grid[cell[1]][cell[0]]
            if summe + number > group[0]:
                return False
        return super().valid_move(cell_x, cell_y, number)
    

class SudokuGUI():
    screen_res = (900,900)
    def __init__(self) -> None:
        self.grid = []
        for x in range(9):
            self.grid.append([])
            for y in range(9):
                self.grid[x].append(0)
        self.gameWindow = pyglet.window.Window(width=900, height=900, resizable=True, vsync=True)
        self.on_draw = self.gameWindow.event(self.on_draw)
        self.batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(0.5,0.5,0.5,1)
    
    def drawGrid(self):
        offset = 45
        lines = []
        WIDTH = 3
        for x in range(10):
            line1 = pyglet.shapes.Line(offset+x*90, 45, offset+x*90, 855, WIDTH, color = (50, 225, 30), batch = self.batch)
            lines.append(line1)
            line1.opacity = 250
        for x in range(10):
            line1 = pyglet.shapes.Line(45, offset+x*90, 855, offset+x*90, WIDTH, color = (50, 225, 30), batch = self.batch)
            lines.append(line1)
            line1.opacity = 250
        
        return lines

    def drawLetter(self, x, y, labels, number):
        label = pyglet.text.Label(str(number), 
                          font_name ='Times New Roman', 
                          font_size = 28, 
                          x = 90 * (x+1) -14 , y = 90 * (y+1) - 14, batch= self.batch) 
        labels.append(label)

    def drawSudokuNumbers(self):
        labels = []
        for x in range(9):
            for y in range(9):
                self.drawLetter(x,y,labels,self.grid[y][x])
        return labels
    
    def on_draw(self):
        self.gameWindow.clear()
        lines = self.drawGrid()
        labels = self.drawSudokuNumbers()
        self.batch.draw()


gui = SudokuGUI()
pyglet.app.run()
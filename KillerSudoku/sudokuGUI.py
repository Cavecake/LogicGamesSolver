import pyglet
import sudoku
import copy

class SudokuGUI():
    screen_res = (900,900)

    SCREEN_COLOR = (1,1,1,1)
    GRID_COLOR = (70,70,70)
    SOLUTION_COLOR = (0,0,204,255)
    NUMBER_COLOR = (0,0,0,255)
    SELECTION_COLOR = (0,0,0,255)
    SELECTION_OPACITY = 70

    def __init__(self) -> None:
        self.selectedCells = []
        self.grid = []
        for x in range(9):
            self.grid.append([])
            for y in range(9):
                self.grid[x].append(0)

        self.solved_grid = copy.deepcopy(self.grid)
        self.solved = False

        self.gameWindow = pyglet.window.Window(width=900, height=900, resizable=True, vsync=True)
        self.batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(*self.SCREEN_COLOR)

        self.multiselect = False

        self.on_draw = self.gameWindow.event(self.on_draw)
        self.on_mouse_press = self.gameWindow.event(self.on_mouse_press)
        self.on_key_press = self.gameWindow.event(self.on_key_press)
        self.on_key_release = self.gameWindow.event(self.on_key_release)
        self.on_mouse_drag = self.gameWindow.event(self.on_mouse_drag)

    def start(self):
        pyglet.app.run()

    def drawGrid(self):
        # creates a 9*9 grid
        offset = 45
        lines = []
        WIDTH = 3
        for x in range(10):
            w = WIDTH
            if x%3 == 0:
                w += 5
            line1 = pyglet.shapes.Line(offset+x*90, 45, offset+x*90, 855, w, color = self.GRID_COLOR, batch = self.batch)
            lines.append(line1)
            line1.opacity = 250
        
        for y in range(10):
            w = WIDTH
            if y%3 == 0:
                w += 5
            line1 = pyglet.shapes.Line(45, offset+y*90, 855, offset+y*90, w, color = self.GRID_COLOR, batch = self.batch)
            lines.append(line1)
            line1.opacity = 250
        
        return lines

    def drawLetter(self, x, y, labels, number, color, font_size = 28, offset = [-14,-14]):
        # helper function
        label = pyglet.text.Label(str(number), 
                          font_name ='Times New Roman', 
                          font_size = font_size, 
                          x = 90 * (x+1) + offset[0] , y = 90 * (y+1) + offset[1], batch= self.batch, color=color) 
        labels.append(label)

    def drawSudokuNumbers(self):
        # populates the sudoku grid with the numbers
        labels = []
        for x in range(9):
            for y in range(9):
                number = self.grid[y][x]
                if number != 0:
                    self.drawLetter(x,8-y,labels,number,self.NUMBER_COLOR)
                    continue
                if self.solved:
                    number = self.solved_grid[y][x]
                    self.drawLetter(x,8-y,labels,number,self.SOLUTION_COLOR)
        return labels
    
    def drawSelection(self):
        # draws the selected cells
        rects = []
        for cell in self.selectedCells:
            x, y = cell
            rect = (46+x*90, 46+ (8-y)*90,
                    88, 88)
            rect = pyglet.shapes.Rectangle(rect[0], rect[1], rect[2], rect[3],self.SELECTION_COLOR, batch=self.batch)
            rect.opacity = self.SELECTION_OPACITY
            rects.append(rect)
        return rects
    
    def drawElements(self):
        objects = []
        objects.append(self.drawSelection())
        objects.append(self.drawGrid())
        objects.append(self.drawSudokuNumbers())
        return objects
    
    def on_draw(self):
        self.gameWindow.clear()
        objects = self.drawElements() # return necessary, because otherwise, pointer from batch will be nullptr
        self.batch.draw()

    def solve(self):
        sud = sudoku.Sudoku(self.grid)
        self.solved_grid = sud.dynamicSolver()
        self.solved = True

    def calcCellCoord(self,x,y):
        # Calc cell coord
        x -= 45
        y -= 45
        x = x - x%90
        y = y - y%90
        x /= 90
        y /= 90
        if x > 8 or y > 8 or y < 0 or x < 0:
            x = None
        return x, 8-y

    def on_mouse_press(self,x, y, button, modifiers):
        x, y = self.calcCellCoord(x,y)
        if x == None:
            return
        
        # selects and deselects cells based on mouse input
        # right Button -> deselect
        # left button -> toggle selection
        # if single select mode only select one at a time
        # multi selection mode can be toggle using the shift key
        # dragging selects all
        if button == pyglet.window.mouse.LEFT:
            if [int(x), int(y)] in self.selectedCells:
                self.deselectCell(int(x),int(y))
                return
            if not self.multiselect:
                self.deselectAll()
            self.selectCell(int(x),int(y))
        elif button == pyglet.window.mouse.RIGHT:
            self.deselectCell(int(x),int(y))
    
    def on_key_press(self,symbol, modifiers):
        if modifiers & pyglet.window.key.MOD_SHIFT:
            self.setMutliselect(True)

        if symbol in [pyglet.window.key.ENTER, pyglet.window.key.RETURN]:
            self.solve()

        if symbol == pyglet.window.key.DELETE or symbol == pyglet.window.key.BACKSPACE:
            self.removeNumbers()

        number = pyglet.window.key.symbol_string(symbol)
        number = number[-1]
        if number in ["1","2","3","4","5","6","7","8","9"]:
            self.setNumber(int(number))

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        x, y = self.calcCellCoord(x,y)
        if x == None:
            return
        self.selectCell(int(x),int(y))

    def on_key_release(self,symbol, modifiers):
        key = pyglet.window.key.symbol_string(symbol)
        if modifiers & pyglet.window.key.MOD_SHIFT or key[1:] == "SHIFT":
            self.setMutliselect(False)

    # Helper functions, to set variables
    def removeNumbers(self):
        for cell in self.selectedCells:
            x, y = cell
            self.grid[y][x] = 0

    def setNumber(self,number):
        for cell in self.selectedCells:
            x, y = cell
            if self.grid[y][x] == number:
                self.grid[y][x] = 0
            else:
                self.grid[y][x] = number

    def setMutliselect(self,state):
        self.multiselect = state

    def selectCell(self,x,y):
        if [x,y] not in self.selectedCells:
            self.selectedCells.append([x,y])

    def deselectAll(self):
        self.selectedCells = []

    def deselectCell(self,x,y):
        if [x,y] in self.selectedCells:
            index = self.selectedCells.index([x,y])
            del self.selectedCells[index]

    def eraseNumber(self):
        for cell in self.selectedCells:
            x, y = cell
            self.grid[y][x] = 0

if __name__ == "__main__":
    gui = SudokuGUI()
    gui.start()
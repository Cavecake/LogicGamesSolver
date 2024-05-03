class Sudoku():

    blocks = [
        [[],[],[]],
        [[],[],[]],
        [[],[],[]]
    ]
    def __init_blocks(self):
        pass
    def __init__(self, grid) -> None:
        self.grid = grid
        self.org_grid = grid
        self.__init_blocks()
    def valid_move(self, cell_x, cell_y, number):
        if self.org_grid[cell_y][cell_x] != 0:
            return False
        
        block = self.get_block(cell_x,cell_y)
        row = self.get_row(cell_y)
        column = self.get_column(cell_x)
        if number in column:
            return False
        if number in row:
            return False
        if number in block:
            return False
        
        return True

    def get_row(self, row_y):
        return self.grid[row_y]
    
    def get_column(self, column_x):
        column = [self.grid[y][column_x] for y in range(9)]
        return column
    
    def get_block(self,cell_x, cell_y):
        top = cell_y - (cell_y % 3)
        left = cell_x - (cell_x % 3)
        block = []
        for x in range(3):
            for y in range(3):
                block.append(self.grid[y+top][x+ left])
        return block
    
    def subSolver(self,x,y):
        if y == 9:
            return True
        
        if self.org_grid[y][x] != 0:
            x1 = (x +1)
            y1 = y
            if x1 == 9:
                x1 = 0
                y1 = y + 1
            if self.subSolver(x1,y1):
                return True
            else:
                self.grid[y][x] = 0

        for i in range(1,10):
            if self.valid_move(x,y,i):
                x1 = x +1
                y1 = y
                if x1 == 9:
                    x1 = 0
                    y1 = y + 1
                self.grid[y][x] = i
                if self.subSolver(x1,y1):
                    return True
                else:
                    self.grid[y][x] = 0

        return False

    def dynamicSolver(self):
        self.subSolver(0,0)
        return self.grid
sod = Sudoku([
    [0,4,1,0,9,2,7,3,8],
    [0,7,6,0,1,0,2,0,0],
    [0,0,2,0,0,0,0,5,0],
    [0,6,0,0,5,1,8,0,4],
    [0,8,3,4,0,0,0,0,0],
    [0,0,0,2,8,0,1,0,0],
    [0,1,0,9,4,0,3,0,0],
    [6,0,0,0,0,8,4,7,5],
    [0,2,8,0,7,0,9,0,6]
])

los = sod.dynamicSolver()

for line in los:
    print(line)
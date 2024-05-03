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
        if self.grid[cell_y][cell_x] != 0:
            return False
        
        for x in range(9):
            if self.grid[cell_y][x] == number:
                return False
            if self.grid[x][cell_x] == number:
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
            x1 = (x +1) % 9
            y1 = y
            if x1 == 9:
                x1 = 0
                y1 = y + 1
            return self.subSolver(x1,y1)

        for i in range(9):
            if self.valid_move(x,y,i):
                x1 = x +1
                y1 = y
                if x1 == 9:
                    x1 = 0
                    y1 = y + 1
                if self.subSolver(x1,y1):
                    return True
                
        return False

    def dynamicSolver(self):
        self.subSolver(0,0)
        return self.grid
sod = Sudoku([
    [0,0,5,0,2,0,0,0,9],
    [4,0,6,8,1,0,0,5,0],
    [0,7,0,0,0,0,3,1,6],
    [5,0,0,2,4,0,6,0,0],
    [0,6,4,0,7,0,2,3,8],
    [1,8,0,3,0,0,0,0,0],
    [6,0,9,0,0,1,8,0,0],
    [7,4,0,9,0,0,0,6,0],
    [0,0,0,7,3,6,0,2,4]
])

los = sod.dynamicSolver()

for line in los:
    print(line)
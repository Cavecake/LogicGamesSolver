import copy
class Sudoku():

    def __init__(self, grid) -> None:
        self.grid = copy.deepcopy(grid)
        self.org_grid = grid

    def valid_move(self, cell_x, cell_y, number):
        # checks if it is valid, to insert a number in a box

        # check if we are allowed to choose a number
        if self.org_grid[cell_y][cell_x] != 0:
            return False
        
        # checks row, block and column
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
        # the block always starts at 0, 3 or 6
        # these are equel to the next smallest multiple of three
        # this can be caluclated by x - (x%3)
        top = cell_y - (cell_y % 3)
        left = cell_x - (cell_x % 3)
        block = []
        for x in range(3):
            for y in range(3):
                block.append(self.grid[y+top][x+ left])
        return block
    
    def subSolver(self,x,y):
        # recursivly creates solution, tries to find solution for the last n - 1 cells
        # from the idea, it finds all valid solutions for the last cell,
        # then for the cell before that
        # it starts in the first cell and moves through the grid, until a solution is found, then returns it, or until the valid move results in a cell with no options
        # then it backtraces, to change the next upper cell

        # In case max depth was reached, the solution was found
        # -> go back up
        if y == 9:
            return True
        
        # If the cell is given by the sudoku, there is only one possibility, call next cell solver
        if self.org_grid[y][x] != 0:
            x1 = (x +1)
            y1 = y
            if x1 == 9:
                x1 = 0
                y1 = y + 1
            return self.subSolver(x1,y1)
    
        # checks all possiblities for the cell
        for i in range(1,10):
            if self.valid_move(x,y,i):
                x1 = x +1
                y1 = y
                if x1 == 9:
                    x1 = 0
                    y1 = y + 1
                self.grid[y][x] = i

                # checks if there is a soultion for the tested possiblity for the last n-1 cells
                if self.subSolver(x1,y1):
                    return True
                else:
                    self.grid[y][x] = 0
        # No solution was found for the last n cells, given the state of the first cells
        return False

    def dynamicSolver(self):
        # dynamic algorithm to solve a sudoku
        self.subSolver(0,0)
        return self.grid
    
if __name__ == "__main__":
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
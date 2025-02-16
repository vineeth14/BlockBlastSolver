from classes import Block, Shape
from image_select import read_shapes_to_grid


def create_shapes(grid):
    shapes = []
    directions = [[0,1],[1,0],[1,1],[-1,-1],[1,-1],[-1,1],[-1,0],[0,-1]]
    #BFS to find all shapes in the grid
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row][col] == 1:
                grid[row][col] = 0
                origin = Block(row,col)
                shape = Shape([origin])
                q = [origin]
                shapes.append(shape)
                while len(q)>0:
                    for i in range(len(q)):
                        block = q.pop()
                        for dr,dc in directions:
                            nr, nc = dr+block.row, dc+block.col
                            if nr in range(grid.shape[0]) and nc in range(grid.shape[1]) and grid[nr][nc] == 1:
                                grid[nr][nc] = 0
                                q.append(Block(nr,nc))
                                shape.segment.append(Block(nr,nc))
                shape.initialize()
    return shapes

grid = read_shapes_to_grid('uncompressed_images/IMG_0437.PNG')
shapes = create_shapes(grid)
 

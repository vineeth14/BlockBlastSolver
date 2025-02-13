import numpy as np
from PIL import Image

image = 'shape_test/BB_Example_2_shape0.png'
def check_color(measured, reference, allowed_deviation):
    correct = True
    for i in range(3): 
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            correct = False
    return correct


def shape_to_grid(image):
    image = Image.open(image) 
    offset = 41 #size of block
    px = image.load()
    tolerance = 30
    background_px = [51,76,132]
    width, height = image.size 
    grid = np.zeros((height//offset,width//offset))
    rows= height//offset
    columns = width//offset

    for x in range(columns):
        block_found = False
        for y in range(1,rows):
            pixel_coord = (x*offset,y*offset)
            current_pixel = px[pixel_coord]
            is_bg_color = check_color(current_pixel,background_px, 0.1)

            if not block_found and not is_bg_color:
                #on first block
                grid[x,y]=1
                block_found=True
            elif block_found and not is_bg_color:
                grid[x,y] =1
            elif block_found and is_bg_color:
                break



    print(grid)


shape_to_grid(image)
from PIL import Image
import numpy as np


def check_color(measured, reference, allowed_deviation):
    correct = True
    for i in range(3):
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            correct = False
    return correct

def read_grid(im):
    offset = 41  # distance between two blocks
    x0 = 10   # can be adapted to the screen dimensions
    width, height = im.size
    px = im.load()
    ref_background = np.array([51, 76, 132])
    grid = np.zeros((height // offset + 2, width // offset + 2))
    x = -1
    while (x + 1) * offset + x0 < width - 1:
        x += 1
        y = 0
        is_background = True
        while (y + 1) * offset < height - 1:
            y += 1
            color_check = check_color(px[x * offset + x0, y * offset], ref_background, 0.1)
            if is_background and not color_check:  # on background but not background color = not on background
                is_background = False
                grid[y, x] = 1
            elif not color_check:  # not on background and not background color = still not on background
                grid[y, x] = 1
            elif not is_background:  # not on background but background color = back on background
                break

    print(grid)
    return grid

read_grid(Image.open('shape_test/BB_Example_2_shape0.png'))
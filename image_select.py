# Testing OpenCV to see if it can detect shapes in the uploaded image
#Split image into 2 parts
# 1.Convert to grayscale
# 2.Apply thresholding to convert the image to binary

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np 
import cv2
import matplotlib.pyplot as plt



image_path ='images_test/BB_Example_5.png'


# def check_color(measured, reference, allowed_deviation):
    # correct = True
    # for i in range(3): 
    #     if abs(measured[i] - reference[i]) > allowed_deviation * 255:
    #         correct = False
    # return correct

def image_to_grid(image_path, grid_size=(8,8)):

    image = Image.open(image_path) 

    grayscale_image = image.convert('L')
    crop_grid = (50, 500, 900, 1300)
    grid_image = grayscale_image.crop(crop_grid)
 
    # grayscale_image.show()
    # Step 3: Apply thresholding to convert the image to binary
    threshold = 85 
    binary_image = grid_image.point(lambda p: 255 if p > threshold else 0)
    # Step 4: Resize the image to the grid size
    resized_image = binary_image.resize(grid_size, Image.NEAREST)

    # Step 5: Convert the image to a NumPy array
    grid = np.array(resized_image)

    # Convert to 0s and 1s
    grid = np.where(grid == 255, 1, 0)

    print(grid)
    return grid




def detect_bottom_shapes(image_path, grid_width=8, grid_height=8):
    image = Image.open(image_path)

    crop_grid = (0, 1400, 900, 1800)
    grid_image = image.crop(crop_grid)
    width, height = grid_image.size

    pictures = 3
    x_width, y_height = grid_image.size

    # Get evenly spaced edges -> Evenly split the image into 3 parts
    edges = np.linspace(0, x_width, pictures + 1)  
    # Cropping images into variables
    cropped_images = []

    for i in range(len(edges) - 1):
        start = edges[i]
        end = edges[i + 1]        
        box = (int(start), 0, int(end), y_height)  # Ensure values are integers
        cropped_shape = grid_image.crop(box)
        # cropped_np = np.array(cropped_shape)
        cropped_images.append(cropped_shape) # Crop the shapes


    return cropped_images

# def read_grid(image):
#     # Convert the supplied image to a PIL Image if it's not already one
#     if not isinstance(image, Image.Image):
#         image = Image.fromarray(image)

#     # Define the region boundaries
#     x_min = 0
#     y_min = 1400
#     x_max = 900
#     y_max = 1800

#     # Load pixel data from the image
#     px = image.load()
#     img_width, img_height = image.size
#     # Define the width and height of the region based on the boundaries
#     region_width = x_max - x_min
#     region_height = y_max - y_min  

#     block_size = 4  # Spacing between grid points (adjust based on your image)
#     x_offset = 10  # Starting horizontal offset

#     ref_background = (48, 74, 139)  # Reference background color

#     # Initialize the grid with zeros (with a small extra buffer)
#     grid = np.zeros((region_height // block_size + 2, region_width // block_size + 2))
#     x = -1
#     while (x + 1) * block_size + x_offset < region_width - 1:
#         print('x', x)
#         x += 1
#         y = 0
#         in_background = True
#         while (y + 1) * block_size < region_height - 1:
#             print(y, y * block_size, region_height)
#             y += 1
#             color_match = check_color(px[x * block_size + x_offset, y * block_size], ref_background, 0.1)
#             if in_background and not color_match:
#                 in_background = False
#                 grid[y, x] = 1
#             elif not color_match:
#                 grid[y, x] = 1
#             elif not in_background:
#                 break

#     return grid

import numpy as np
from PIL import Image

def check_color(measured, reference, allowed_deviation):
    correct = True
    for i in range(3): 
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            correct = False
    return correct

def average_block_color(px, x_start, y_start, block_size, img_width, img_height):
    """
    Returns the (R, G, B) average color of the block_size x block_size region
    starting at (x_start, y_start). Ensures we stay within image bounds.
    """
    r_total, g_total, b_total = 0, 0, 0
    count = 0
    
    # Clamp the region so we don't go outside the image
    x_end = min(x_start + block_size, img_width)
    y_end = min(y_start + block_size, img_height)

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            r, g, b = px[x, y]
            r_total += r
            g_total += g
            b_total += b
            count += 1

    if count == 0:
        return (0, 0, 0)
    return (r_total / count, g_total / count, b_total / count)

def read_grid(image):
    # Convert the supplied image to a PIL Image if it's not already one
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    
    # Define the region boundaries
    x_min, y_min = 0, 0
    x_max, y_max = image.width, image.height
    region_width = x_max - x_min
    region_height = y_max - y_min

    # Load pixel data from the image
    px = image.load()
    img_width, img_height = image.size

    block_size = 46  # Size of each block region
    x_offset = 30    # Starting horizontal offset

    ref_background = (51, 75, 131)  # Reference background color

    # Initialize the grid (with a small extra buffer)
    rows = region_height // block_size + 2
    cols = region_width // block_size + 2
    grid = np.zeros((rows, cols))

    x = -1
    while (x + 1) * block_size + x_offset < region_width - 1:
        x += 1
        y = 0
        in_background = True

        while (y + 1) * block_size < region_height - 1:
            y += 1

            # Calculate the top-left corner of this block region in full image coordinates
            x_start = x_min + x_offset + x * block_size
            y_start = y_min + y * block_size

            # Get the average color of this block region
            avg_col = average_block_color(px, x_start, y_start, block_size, img_width, img_height)
            # Use your check_color function with an allowed deviation (e.g., 0.1)
            is_background = check_color(avg_col, ref_background, allowed_deviation=0.1)

            if in_background and not is_background:
                # Transitioned from background to block
                in_background = False
                grid[y, x] = 1
            elif not is_background:
                # Still within a block
                grid[y, x] = 1
            elif not in_background:
                # Transitioned back to background
                break

    return grid

image_path ='images_test/BB_Example_0.png'


shapes =detect_bottom_shapes(image_path)
# for shape in shapes:
#     shape.show()
#     grid = shape_to_grid(shape)
#     print(grid)

image = Image.open(image_path)

x_min=0
y_min=1400
x_max=900
y_max=1800
crop_grid = (x_min, y_min, x_max, y_max)
grid_image = image.crop(crop_grid)

# grid =shape_to_grid(grid_image)

# print(grid)
# image_to_binary_grid(shapes[2])
# shapes[0].show()
# shapes[0].save('shape_test/BB_Example_1_shape0.jpeg')


grid = read_grid(grid_image)
print(grid)


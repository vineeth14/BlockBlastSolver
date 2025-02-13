# Testing OpenCV to see if it can detect shapes in the uploaded image
#Split image into 2 parts
# 1.Convert to grayscale
# 2.Apply thresholding to convert the image to binary

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np 
import cv2
import matplotlib.pyplot as plt



image_path ='images_test/BB_Example_5.png'


def check_color(measured, reference, allowed_deviation):
    correct = True
    for i in range(3): 
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            correct = False
    return correct

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

def find_x0(image, background_px, tolerance):
    """Finds the starting x0 position dynamically based on the first non-background pixel."""
    px = image.load()
    width, height = image.size
    
    for x in range(width):
        first_pixel = px[x, height // 2]  # Check a row in the middle
        if not check_color(first_pixel, background_px, tolerance):
            return x  # The first non-background pixel
    return 10  # Default fallback value

def shape_to_grid(image):
    # image = Image.open(image) 
    image = image.resize((685,228))
    offset = 41 #size of block 
    px = image.load()
    tolerance = 0.05
    background_px = [51,76,132]
    x0 = 10
    width, height = image.size 
    rows= (height)//offset
    columns = (width-x0)//offset
    grid = np.zeros((rows+2, columns+2))


    for x in range(columns):

        block_found = False
        for y in range(0,rows):

            pixel_coord = (x*offset+x0,y*offset)
            current_pixel = px[pixel_coord]
            is_bg_color = check_color(current_pixel,background_px, tolerance)
            if not block_found and not is_bg_color:
                #on first block
                grid[y,x] = 1
                block_found=True
            elif block_found and not is_bg_color:
                grid[y,x] = 1
            elif block_found and is_bg_color:
                break
    
    return grid


def shape_to_grid_2(image):
    offset = 41  # distance between two blocks
    x0 = 10  # can be adapted to the screen dimensions
    x = -1
    background_ref = (48, 74, 139)
    grid = np.zeros(((y_max - y_min) // offset + 2, (x_max - x_min) // offset + 2))  # the 2 may be changed for fine-tuning of pixels
    while (x + 1) * offset + x0 < (x_max - x_min) - 1:
        x += 1
        y = 0
        background = True
        while (y + 1) * offset < (y_max - y_min) - 1:
            # print(y, y * offset + y_min)
            y += 1
            check_color = check_color(px[x * offset + x0, y * offset], background_ref, 0.1)
            if background and not check_color:  # on the background but not the background color = not on the background
                background = False
                grid[y, x] = 1
            elif not check_color:  # not on the background and not the background color = still not on the background
                grid[y, x] = 1
            elif not background:  # not on the background but background color = back on the background
                break
    return grid


image_path ='images_test/BB_Example_1.png'


shapes =detect_bottom_shapes(image_path)
# for shape in shapes:
#     shape.show()
#     grid = shape_to_grid(shape)
#     print(grid)

image = Image.open(image_path)

crop_grid = (0, 1400, 900, 1800)
grid_image = image.crop(crop_grid)
# grid_image.show()
grid =shape_to_grid(grid_image)

print(grid)
# image_to_binary_grid(shapes[2])
# shapes[0].show()
# shapes[0].save('shape_test/BB_Example_1_shape0.jpeg')


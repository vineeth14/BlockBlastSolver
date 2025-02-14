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

def read_grid(image):
    # Convert the supplied image to a PIL Image if it's not already one
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)

    # Define the region boundaries
    x_min = 0
    y_min = 1400
    x_max = 900
    y_max = 1800

    # Load pixel data from the image
    px = image.load()
    img_width, img_height = image.size
    # Define the width and height of the region based on the boundaries
    region_width = x_max - x_min
    region_height = y_max - y_min  

    block_size = 46  # Spacing between grid points (adjust based on your image)
    x_offset = 10  # Starting horizontal offset

    ref_background = (48, 74, 139)  # Reference background color

    # Initialize the grid with zeros (with a small extra buffer)
    grid = np.zeros((region_height // block_size + 2, region_width // block_size + 2))
    x = -1
    while (x + 1) * block_size + x_offset < region_width - 1:
        print('x', x)
        x += 1
        y = 0
        in_background = True
        while (y + 1) * block_size < region_height - 1:
            print(y, y * block_size, region_height)
            y += 1
            color_match = check_color(px[x * block_size + x_offset, y * block_size], ref_background, 0.1)
            if in_background and not color_match:
                in_background = False
                grid[y, x] = 1
            elif not color_match:
                grid[y, x] = 1
            elif not in_background:
                break

    return grid

image_path ='images_test/BB_Example_4.png'


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


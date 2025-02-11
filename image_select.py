# Testing OpenCV to see if it can detect shapes in the uploaded image
#Split image into 2 parts
# 1.Convert to grayscale
# 2.Apply thresholding to convert the image to binary

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np 
import cv2
import matplotlib.pyplot as plt



image_path ='images_test/BB_Example_2.jpeg'

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
    print(height, width)


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
        cropped_images.append(grid_image.crop(box)) # Crop the shapes


    return cropped_images





shapes =detect_bottom_shapes(image_path)
# image_to_binary_grid(shapes[2])
shapes[0].show()
shapes[2].save('images_test/BB_Example_2_shape2.jpeg')


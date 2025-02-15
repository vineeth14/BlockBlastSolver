# Testing OpenCV to see if it can detect shapes in the uploaded image
#Split image into 2 parts
# 1.Convert to grayscale
# 2.Apply thresholding to convert the image to binary

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np 
import cv2
import matplotlib.pyplot as plt



image_path ='uncompressed_images/IMG_0437.PNG'


def image_to_grid(image_path, grid_size=(8,8)):

    image = Image.open(image_path) 

    grayscale_image = image.convert('L')
    crop_grid = (50, 600, 1120, 1650)
    grid_image = grayscale_image.crop(crop_grid)
   
    # Step 3: Apply thresholding to convert the image to binary
    threshold = 85 
    binary_image = grid_image.point(lambda p: 255 if p > threshold else 0)

    # Step 4: Resize the image to the grid size
    resized_image = binary_image.resize(grid_size, Image.NEAREST)

    # Step 5: Convert the image to a NumPy array
    grid = np.array(resized_image)

    # Convert to 0s and 1s
    grid = np.where(grid == 255, 1, 0)

    return grid

# The function returns True if the pixel color is close to the background color, and False if it's different.

def check_color(measured, reference, allowed_deviation):
    flag = True
    for i in range(3): 
        # Check if the difference between measured and background color is greater than the allowed deviation
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            flag = False
    return flag

def read_shapes_to_grid(image):
    image = Image.open(image_path)
    # Convert the supplied image to a PIL Image if it's not already one
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    

    # Define the region boundaries
    x_min = 100
    y_min = 1700
    x_max = 1070
    y_max = 2200
    crop_grid = (x_min, y_min, x_max, y_max)
    grid_image = image.crop(crop_grid)

    # Load pixel data from the image
    px = grid_image.load()
    img_width, img_height = grid_image.size


    x_offset = 10
    block_size = 58  # Make sure this matches your grid size

    ref_background = (48, 74, 139)  # Reference background color

    # Sample points focused on block centers and edges
    # Defines multiple points to sample within each grid cell

    sample_offsets = [
        (0, 0),     # Center
        (5, 0),     # Near right
        (-5, 0),    # Near left
        (0, 5),     # Near down
        (0, -5),    # Near up
        (15, 0),    # Far right
        (-15, 0),   # Far left
        (0, 15),    # Far down
        (0, -15),   # Far up
        (0, 20),    # Extra far down
        (0, -20),   # Extra far up    
    ]
      
    # Initialize the grid with zeros (with a small extra buffer)
    grid = np.zeros((img_height // block_size + 2, img_width // block_size + 2))
    x = -1
    while (x + 1) * block_size + x_offset < img_width - 1:
        x += 1
        y = 0
        in_background = True
        while (y + 1) * block_size < img_height - 1:
            y += 1
            
            # Sample multiple pixels in each block
            base_x = x * block_size + x_offset
            base_y = y * block_size
            
            # Count both block and background pixels
            bg_pixels = 0
            block_pixels = 0
            total_samples = len(sample_offsets)
            
            for offset_x, offset_y in sample_offsets:
                try:
                    sample_x = base_x + offset_x
                    sample_y = base_y + offset_y
                    if 0 <= sample_x < img_width and 0 <= sample_y < img_height:
                        color_match = check_color(px[sample_x, sample_y], ref_background, 0.05)
                        if color_match:
                            bg_pixels += 1
                        else:
                            block_pixels += 1
                except IndexError:
                    total_samples -= 1  # Reduce total if pixel is out of bounds
                    continue
            
            # Use ratio of block pixels to total valid samples
            block_ratio = block_pixels / total_samples
            is_background = block_ratio < 0.4  # If less than 40% of pixels are block pixels
            
            if in_background and not is_background:
                in_background = False
                grid[y, x] = 1
            elif not is_background:
                grid[y, x] = 1
            elif not in_background and bg_pixels > total_samples * 0.7:
                break

    return grid

image_path ='uncompressed_images/IMG_0436.PNG'


grid = image_to_grid(image_path)
print(grid)

shape_grid = read_shapes_to_grid(image_path)
print(shape_grid)




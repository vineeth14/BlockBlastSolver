  #!/usr/bin/env python3

# Testing OpenCV to see if it can detect shapes in the uploaded image
#Split image into 2 parts
# 1.Convert to grayscale
# 2.Apply thresholding to convert the image to binary

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np 
import cv2
import matplotlib.pyplot as plt



# image_path ='uncompressed_images/IMG_0437.PNG'


def image_to_grid(image_path, grid_size=(8,8)):

    image = Image.open(image_path) 

    grayscaleImage = image.convert('L')
    cropGrid = (50, 600, 1120, 1650)
    gridImage = grayscaleImage.crop(cropGrid)
   
    # Step 3: Apply thresholding to convert the image to binary
    threshold = 85 
    binaryImage = gridImage.point(lambda p: 255 if p > threshold else 0)

    # Step 4: Resize the image to the grid size
    resizedImage = binaryImage.resize(grid_size, Image.NEAREST)

    # Step 5: Convert the image to a NumPy array
    board = np.array(resizedImage)

    # Convert to 0s and 1s
    board = np.where(board == 255, 1, 0)

    return board

# The function returns True if the pixel color is close to the background color, and False if it's different.

def check_color(measured, reference, allowed_deviation):
    flag = True
    for i in range(3): 
        # Check if the difference between measured and background color is greater than the allowed deviation
        if abs(measured[i] - reference[i]) > allowed_deviation * 255:
            flag = False
    return flag

def read_shapes_to_grid(image):
    image = Image.open(image)
    # Convert the supplied image to a PIL Image if it's not already one
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    

    # Define the region boundaries
    x_min = 100
    y_min = 1700
    x_max = 1070
    y_max = 2200
    cropGrid = (x_min, y_min, x_max, y_max)
    gridImage = image.crop(cropGrid)

    # Load pixel data from the image
    px = gridImage.load()
    imgWidth, imgHeight = gridImage.size


    xOffset = 10
    blockSize = 58  # Make sure this matches your grid size

    refBackground = (48, 74, 139)  # Reference background color

    # Sample points focused on block centers and edges
    # Defines multiple points to sample within each grid cell

    sampleOffsets = [
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
    grid = np.zeros((imgHeight // blockSize + 2, imgWidth // blockSize + 2))
    x = -1
    while (x + 1) * blockSize + xOffset < imgWidth - 1:
        x += 1
        y = 0
        ShapeDetected = False
        while (y + 1) * blockSize < imgHeight - 1:
            y += 1
            
            # Sample multiple pixels in each block
            baseX = x * blockSize + xOffset
            baseY = y * blockSize
            
            # Count both block and background pixels
            bgPixels = 0
            blockPixels = 0
            totalSamples = len(sampleOffsets)
            
            for offsetX, offsetY in sampleOffsets:
                try:
                    sampleX = baseX + offsetX
                    sampleY = baseY + offsetY
                    if 0 <= sampleX < imgWidth and 0 <= sampleY < imgHeight:
                        colorMatch = check_color(px[sampleX, sampleY], refBackground, 0.05)
                        if colorMatch:
                            bgPixels += 1
                        else:
                            blockPixels += 1
                except IndexError:
                    totalSamples -= 1  # Reduce total if pixel is out of bounds
                    continue
            
            # Use ratio of block pixels to total valid samples
            blockRatio = blockPixels / totalSamples
            isBackground = blockRatio < 0.4  # If less than 40% of pixels are block pixels
            
            if not ShapeDetected and not isBackground:
                ShapeDetected = True
                grid[y, x] = 1
            elif not isBackground:
                grid[y, x] = 1
            elif ShapeDetected and bgPixels > totalSamples * 0.7:
                break

    return grid

# image_path ='uncompressed_images/IMG_0435.PNG'


# board = image_to_grid(image_path)
# print(board)

# shape_grid = read_shapes_to_grid(image_path)
# print(shape_grid)




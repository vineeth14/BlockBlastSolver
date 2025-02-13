import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import image_select

def remove_background(shapes):
    # Define the background RGB color (given by user)
    bg_color = np.array([51, 76, 132])  # Adjusted for the provided background color

    # Tolerance for color detection
    tolerance = 30
    lower_bound = np.clip(bg_color - tolerance, 0, 255) #np clip ensures that the values are within the valid range
    upper_bound = np.clip(bg_color + tolerance, 0, 255)

    processed_images = []
    for shape in shapes:
        # Load the image and check if it was successfully loaded
        image_rgb = cv2.cvtColor(shape, cv2.COLOR_BGR2RGB)

        # Create a mask where the background is detected
        mask = cv2.inRange(image_rgb, lower_bound, upper_bound)
        mask_inv = cv2.bitwise_not(mask)  # Invert mask to keep the foreground

        # Convert image to RGBA
        image_rgba = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2RGBA)
        image_rgba[:, :, 3] = mask_inv  # Assign the inverted mask to the alpha channel

        processed_images.append(image_rgba)

    return processed_images
        

def extract_shape(image_rgba):
    """Extracts the shape from an image after background removal."""

    
    # Convert RGBA to grayscale using the alpha channel
    alpha_channel = image_rgba[:, :, 3]

    # Create a binary mask
    _, binary_mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank mask with the same shape
    mask = np.zeros_like(alpha_channel)

    # Draw the largest contour on the mask
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

    # Apply mask to extract the shape
    extracted_shape = cv2.bitwise_and(image_rgba, image_rgba, mask=mask)

    return extracted_shape




image_path = 'images_test/BB_Example_1.png'
shapes =image_select.detect_bottom_shapes(image_path)

processed_images = remove_background(shapes)
e = extract_shape(processed_images[0])
Image.fromarray(e).show()
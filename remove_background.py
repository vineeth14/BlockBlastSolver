import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image_paths = ['BB_Example_1_shape0.jpeg', 'BB_Example_2_shape0.jpeg', 'BB_Example_6_shape0.jpeg', 'BB_Example_7_shape1.jpeg', 'BB_Example_6_shape1.jpeg', 'BB_Example_7_shape2.jpeg',
'BB_Example_1_shape1.jpeg', 'BB_Example_2_shape1.jpeg', 'BB_Example_6_shape2.jpeg', 'BB_Example_1_shape2.jpeg', 'BB_Example_2_shape2.jpeg', 'BB_Example_7_shape0.jpeg']

def remove_background(image_paths):
    # Define the background RGB color (given by user)
    bg_color = np.array([51, 76, 132])  # Adjusted for the provided background color

    # Tolerance for color detection
    tolerance = 30
    lower_bound = np.clip(bg_color - tolerance, 0, 255)
    upper_bound = np.clip(bg_color + tolerance, 0, 255)

    processed_images = []

    # Use the script's directory to form an absolute path, ensuring we write in the correct location.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_dir, 'shape_extracted')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for img_path in image_paths:
        # Load the image and check if it was successfully loaded
        image = cv2.imread(img_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a mask where the background is detected
        mask = cv2.inRange(image_rgb, lower_bound, upper_bound)
        mask_inv = cv2.bitwise_not(mask)  # Invert mask to keep the foreground

        # Convert image to RGBA
        image_rgba = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2RGBA)
        image_rgba[:, :, 3] = mask_inv  # Assign the inverted mask to the alpha channel

        # Save the output image in the shape_extracted folder
        base_name = os.path.basename(img_path)
        output_file = os.path.join(output_folder, base_name.replace('.jpeg', '_no_bg.png'))
        success = cv2.imwrite(output_file, image_rgba)
        if not success:
            print(f'Error: Could not write file {output_file}')
        else:
            # Load for displaying
            processed_images.append(Image.open(output_file))

    # Display the processed images
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))

    for ax, img, name in zip(axes.ravel(), processed_images, image_paths):
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(os.path.basename(name))

    plt.show()

remove_background(image_paths)
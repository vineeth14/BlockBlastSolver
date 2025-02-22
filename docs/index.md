---
layout: default
title: Block Blast Solver 
---

# Building Block Blast Solver:

## Introduction
This project started with a simple obsession— [Block Blast](https://apps.apple.com/us/app/block-blast/id1617391485). The challenge of maximizing my score was fun, and I started a friendly competition with my friends. This got me thinking of whether I could build a solver.

"Block Blast is a puzzle game that challenges you to fit different block shapes onto a grid, clearing lines to score points. The game’s simplicity is its charm, but don’t be fooled—mastering Block Blast takes skill, strategy, and a sharp mind."

I wanted a program that could analyze a screenshot when I was stuck and suggest the best moves. 
I decided to stay away from using AI as that seemed to defeat the purpose of the challenge.

## Challenges Faced

The development process came with several interesting challenges:
- **Game State Recognition**: Block blast does not have a defined set of shapes like for example tetris. Capturing and understanding the game state accurately, including different block colors and patterns
- **Game Logic**: Block blast has a unique game logic that requires a custom approach to solving the game. 
- **Performance Optimization**: Finding the right balance between speed and accuracy while managing computational resources

## Game State Recognition

- The first challenge was to capture the game state accurately. I started with the following approach:

Goal: To find the simplest solution to converting the uploaded image of the game board and the blocks within it to 0s and 1s respectively.

Approach 1: Simple Image Processing

Use image processing to crop the image into 2 parts, the game board and the game pieces.
I came up with the following approach: 
1. Crop image into 2 parts, the game board and the game pieces.
2. Convert Image to Grayscale. 
3. Crop Image to Isolate Region of Interest. 
4. Apply Binary Thresholding to convert Grayscale to black and white. 
5. Resize Binary Image to a smaller grid (e.g., 8x8). 
6. Convert Resized image to NumPy Array where any pixel value of 255 is converted to 1.


This approach worked well for the game board. However, it was not able to capture the game pieces accurately.

Reasons why the first method doesn’t work here. 

- Inconsistent results as shapes can be different shades of blue. Background color is a shade of blue so it makes it difficult to do a simple image processing and get a consistent binary image. 


So I needed a better approach to capture the game pieces accurately.

Approach 2: Using HSV Ranges 

Attempted using HSV ranges to extract the shapes from the cropped images:
- This doesn’t work because I suspect that some of the colors used are randomly generated or that the number of colors used is larger than I cared to manually identify.
- So hard coding the values wouldn’t work consistently.

Final Approach: Color Detection

This worked well to identify the game pieces.
- Use color detection to extract the shapes from the cropped images. 
- I used a grid based approach to calculate rows and columns based on the image dimensions. I then loop through the each column and compare the current position’s pixel RGB with the background color rgb reference.

This proved to be quite challenging as it was quite difficult get consistent results with this approach. It was easy to find the shape. Accurately obtaining the correct number of blocks and the shape was extremely inconsistent. Due to a number of factors ( Image quality, Resolution etc).

To improve the accuracy of block detection, I learned and applied a number of techniques.
1. More sophisticated shape detection :- 
    1. Sample multiple points in current block 
    2. Count both block and background pixels 
    3. Use ratio of block pixels to total valid samples

This process repeats for each grid cell, building up a binary representation of where shapes are located. The multiple sampling points help make the detection robust against:
- Noise in the image
- Shape edges
- Small variations in color
- Partial shapes


## Approach to Game Logic

The solution evolved through several iterations:

- **Board Representation**: Using a 2D array structure to represent the game board, optimized for quick pattern matching
- **Pattern Recognition**: Implementing efficient algorithms to identify matching patterns and potential moves
- **Move Generation**: Developing a strategy to generate and prioritize moves based on their potential impact

## What Didn't Work & Lessons Learned

Some approaches that didn't pan out:

- Initial attempts at pure image recognition proved too slow for real-time gameplay
- Early optimization efforts focused on the wrong bottlenecks
- These failures led to our current, more efficient solution

## Current Solution & Future Plans

The current implementation successfully:
- Captures game state in real-time
- Identifies optimal moves quickly
- Executes moves with proper timing

Future improvements will focus on:
- Enhanced pattern recognition
- Better handling of special game pieces
- Improved performance optimization

[View Project on GitHub](https://github.com/yourusername/blockblast_solver) 
---
layout: default
title: Block Blast Solver 
---

# Building a Block Blast Solver

## Introduction

This project started with a simple obsession—[Block Blast](https://apps.apple.com/us/app/block-blast/id1617391485). The challenge of maximizing my score was fun, and I started a friendly competition with my friends to see who could get the highest score. This got me thinking of whether I could build a solver that could give me the best possible moves.

<blockquote class="highlight">
Block Blast is a puzzle game that challenges you to fit different block shapes onto a grid, clearing lines to score points. The game's simplicity is its charm, but don't be fooled—mastering Block Blast takes skill, strategy, and a sharp mind.
</blockquote>

I wanted a program that could analyze a screenshot when I was stuck and suggest the best moves. I decided to stay away from using AI as that seemed to defeat the purpose of the challenge.

## Challenges Faced

The development process came with several interesting challenges:

| Challenge | Description |
|-----------|-------------|
| Game State Recognition | Block Blast does not have a defined set of shapes like Tetris. Capturing and understanding the game state accurately, including different block colors and patterns. |
| Game Logic | Block Blast has a unique game logic that requires a custom approach to solving the game. |
| Performance Optimization | Finding the right balance between speed and accuracy while managing computational resources. |

## Game State Recognition

The first challenge was to capture the game state accurately. I started with the following approach:

### Goal
> To find the simplest solution to converting the uploaded image of the game board and the blocks within it to 0s and 1s respectively.

### Approach 1: Simple Image Processing

1. Crop image into 2 parts: the game board and the game pieces
2. Convert image to grayscale
3. Crop image to isolate the region of interest
4. Apply binary thresholding to convert grayscale to black and white
5. Resize binary image to a smaller grid (e.g., 8x8)
6. Convert resized image to a NumPy array where any pixel value of 255 is converted to 1

#### Visual demonstration of the process:

<div style='display: flex; gap: 30px; align-items: center; justify-content: center; margin: 20px 0; background-color: #f5f5f5; padding: 20px; border-radius: 8px;'>
  <div style='text-align: center;'>
    <img src='pictures/game_ss.png' alt='Original Game State' style='width:150px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p style='margin-top: 10px; font-weight: bold;'>Step 1: Original Screenshot</p>
  </div>
  
  <div style='color: #666; font-size: 24px;'>→</div>
  
  <div style='text-align: center;'>
    <img src='pictures/grayscale_board.png' alt='Grayscale Conversion' style='width:150px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p style='margin-top: 10px; font-weight: bold;'>Step 2: Grayscale</p>
  </div>
  
  <div style='color: #666; font-size: 24px;'>→</div>
  
  <div style='text-align: center;'>
    <img src='pictures/binary_board.png' alt='Binary Threshold' style='width:150px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
    <p style='margin-top: 10px; font-weight: bold;'>Step 3: Binary</p>
  </div>
  
  <div style='color: #666; font-size: 24px;'>→</div>
  
  <div style='text-align: center;'>
    <pre style='background-color: #fff; padding: 15px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-family: monospace; margin: 0;'>[[1 1 1 0 0 0 0 1]
[0 0 0 0 0 0 0 1]
[0 0 0 0 0 0 0 1]
[0 0 0 0 0 0 0 0]
[0 0 0 0 0 0 0 0]
[0 0 0 0 0 0 0 0]
[0 1 1 0 0 0 0 0]
[0 1 1 0 0 0 0 0]]</pre>
    <p style='margin-top: 10px; font-weight: bold;'>Final Matrix</p>
  </div>
</div>

### Approach Evolution

#### Why the first method failed for game pieces:
- Inconsistent results as shapes can be different shades of blue
- Background color interference made simple image processing unreliable

- Inconsistent results as shapes can be different shades of blue. The background color is a shade of blue, making it difficult to do simple image processing and get a consistent binary image.

### Approach 2: Using HSV Ranges

Attempted using HSV ranges to extract the shapes from the cropped images:

- This doesn't work because I suspect that some of the colors used are randomly generated or that the number of colors used is larger than I cared to manually identify.
- So hard coding the values wouldn't work consistently.

### Final Approach: Color Detection

After trying the above approaches, I decided to develop a color detection system to extract the shapes from the cropped images that would work consistently.
This proved to be quite challenging as it was difficult to get consistent results with this approach. It was easy to find the shape, but accurately obtaining the correct number of blocks and the shape was extremely inconsistent due to factors like image quality and resolution. I applied a number of techniques to improve the accuracy of the detection.

#### Grid-Based Scanning
- The game board is divided into a grid where each cell represents a potential block position.
- Each cell is scanned systematically using a fixed block size (58 pixels) and small offset (10 pixels). 
- This creates a consistent sampling pattern regardless of the board's current state.

#### Multi-Point Sampling Strategy
- Instead of relying on a single pixel, each grid cell is sampled at 11 strategic points.
- This multi sample approach helps handling color variations and potential image noise.

#### Color Matching Algorithm
For each sampled point:
1. Compare the pixel's RGB values against a reference background color (48, 74, 139)
2. Count both background matches and block (non-background) matches
3. Calculate a ratio of block pixels to total valid samples
4. Consider a cell to contain a block if more than 40% of samples are non-background

---

## Approach to Game Logic

### Does the game make us lose on purpose?

I say this because at the beginning of a game, we can very clearly see that the proposed pieces are strangely perfect—they are exactly the pieces needed to complete a row or a column. So, the game is clearly aware of the pieces we need, and at the start of the game at least, it helps us. This was an interesting observation I noticed.

### Solution Evolution

The solver uses:

1. **Board Representation**
   - 2D array structure
   - Optimized pattern matching

The final strategy I developed is that for each piece, we test all possible positions where it can be placed and assign a score to each position.

### Scoring Methodology

| Factor | Impact |
|--------|---------|
| Neighbors | Increase score plus for each neighbor |
| Border placement | Increase score plus for each border placement |
| Completed rows/columns | Reward a bonus of 50 points|
| Isolated blocks | Score penalty |
| Holes | Score penalty |



The best position for each piece that will yield the highest score, we go through all possible positions for all pieces in all possible orders. Piece 1, then 2, then 3, then 1, then 3, then 2, etc. This is therefore a brute-force method, which takes a lot of time, especially when there are few pieces already placed on the board.

So, I added the below optimization:

- At the very beginning of the game, this is not performed. It is only done once at least 15 squares have been placed on the board, as doing it earlier would take too much time and also has no real value when there are no pieces yet.

**Lessons Learned**:

- I initially tried to improve the scoring methodology by increasing the score for partially completed rows/columns. This led to over-rewarding boards that have many filled cells even when they are not close to becoming complete. This can mislead the solver into choosing moves that rack up a lot of temporary points without actually progressing toward clearing rows/columns.

### Future Improvements
- [ ] Enhanced pattern recognition
- [ ] Special piece handling
- [ ] Performance optimization

[View Project on GitHub](https://github.com/vineeth14/BlockBlastSolver) 
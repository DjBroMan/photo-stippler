# Photo to Dot - Stippling Art Generator

A Python project that converts photographs into stippled dot art representations using computer vision and interactive visualization.

## Overview

This project generates stippling patterns from images, where darker areas contain more dots and lighter areas contain fewer dots. The resulting artwork is visualized interactively using Pygame, with animated point movements and various interactive features.

## Features

- **Automatic Stippling Generation**: Converts images to stippled dot patterns using density-based point distribution
- **Interactive Visualization**: Real-time visualization of stippling points in a Pygame window
- **Point Animation**: Watch points move to their target positions with smooth animations
- **Multiple Point Behaviors**: 
  - Point following (chase behavior)
  - Mouse following (interactive control)
  - Random movement patterns
- **Persistent Storage**: Saves generated stippling data to JSON for later use

## Project Structure

```
.
├── main.py              # Main entry point with Pygame visualization
├── strippling.py        # Stippling generation algorithm
├── Point.py             # Point class for individual dots
├── Vector.py            # Vector math utilities
├── movePoints.py        # Point movement behaviors
├── point_follow.py      # Chase/follow behavior
├── mouse_follow.py      # Mouse tracking behavior
├── test.py              # Testing utilities
├── requirements.txt     # Python dependencies
├── images/              # Input image folder
└── stipplings/          # Generated stippling data (JSON format)
```

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies (numpy, opencv-python, pygame)

## Installation

1. Clone or download this project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your images in the `images/` folder (supports .png, .jpg, .jpeg)
2. Run the main application:
   ```bash
   python main.py
   ```
3. Interact with the visualization using your mouse and keyboard

## How It Works

### Stippling Algorithm

The stippling generation process:
1. Loads an image and converts it to grayscale
2. Applies Gaussian blur for smoothing
3. Creates a density map (darker pixels = higher density)
4. Distributes points based on weighted density sampling
5. Iteratively optimizes point positions to better match image density
6. Stores the final point configuration in JSON format

### Visualization

The Pygame window displays:
- Animated dots moving to their target positions
- Interactive control modes (follow mouse, chase behavior, etc.)
- Real-time rendering of the stippling artwork

## Customization

Key settings in `main.py`:
- `WIDTH`, `HEIGHT`: Window dimensions (default: 1000x800)
- `POINT_COLOR`: Color of the dots (default: cyan)
- `BG`: Background color (default: black)

Settings in `strippling.py`:
- `NUM_POINTS`: Number of dots to generate (default: 6000)
- `ITERATIONS`: Optimization iterations (default: 25)

## Dependencies

- **numpy**: Numerical computations and array operations
- **opencv-python**: Image processing and density calculation
- **pygame**: Interactive visualization

## License

This project is for personal use and experimentation.

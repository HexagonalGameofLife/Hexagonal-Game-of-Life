# Hexagonal Game of Life

## Overview

The Hexagonal Game of Life is an adaptation of Conway’s Game of Life that uses a hexagonal grid instead of the traditional square grid. This project showcases a simulation implemented in Python, using libraries such as pygame for visualization and numpy for grid management. The unique properties of hexagonal grids allow for a more balanced and natural representation of cellular automata, as explored in the accompanying research paper.

## Repository Structure

main.py: The Python script containing the implementation of the Hexagonal Game of Life. This includes the grid initialization, hexagonal calculations, neighbor detection, and simulation rules.

Hexagonal.pdf: A comprehensive research paper detailing the theory, methodology, experiments, and findings related to the Hexagonal Game of Life.

## Features

Simulation Features

Dynamic Grid Visualization: Hexagonal cells are dynamically drawn on the screen using pygame.

User Interaction:

Click on cells to toggle their state between alive and dead.

Control the simulation using buttons:

Start/Pause: Begin or halt the simulation.

Next Step: Advance the simulation by one generation.

Clear: Reset the grid to an empty state.

Random: Populate the grid with a random initial configuration.

Rule Adaptation: Implements Conway’s rules modified for hexagonal grids, ensuring accurate neighbor calculations and pattern evolution.

## Research Insights

Explores the differences between square and hexagonal grids in cellular automata.

Analyzes unique behaviors such as oscillators, methuselah patterns, and the absence of still-life patterns in hexagonal grids.

Investigates rule modifications and their effects on pattern dynamics.

## Getting Started

Prerequisites

Ensure you have the following installed:

Python 3.7 or higher

pygame library

numpy library

Install the required libraries using:

pip install pygame numpy

Running the Simulation

Clone the repository or download the main.py file.

Run the simulation using the command:

python main.py

Interact with the simulation using the GUI buttons and observe the evolution of patterns on the hexagonal grid.

How It Works

Grid Structure

The hexagonal grid is represented as a 2D matrix.

Each cell has six neighbors, calculated based on column-parity checks to account for the hexagonal structure.

Rules

The rules of the Hexagonal Game of Life are adapted from Conway’s rules:

Underpopulation: A live cell with fewer than two neighbors dies.

Survival: A live cell with two or three neighbors survives.

Overpopulation: A live cell with more than three neighbors dies.

Reproduction: A dead cell with exactly two neighbors becomes alive.

Key Functions

draw_grid: Renders the hexagonal grid on the screen.

get_neighbors: Calculates the neighbors for a given cell in the hexagonal structure.

update_grid: Updates the grid based on the rules of the game.

random_pattern: Fills the grid with a random pattern.

clear_grid: Resets the grid to an empty state.

Research Highlights

Experimentation

Initial configurations such as oscillators, methuselahs, and random patterns were tested.

Rule modifications were explored to analyze their impact on grid behavior.

Findings

Hexagonal grids do not produce stable (still-life) patterns, leading to more dynamic systems.

Oscillators and moving patterns exhibit unique characteristics compared to square grids.

The symmetry of hexagonal grids enhances the precision of neighbor-based interactions.

Future Directions

Machine Learning Integration: Use AI to detect and optimize patterns.

Large-Scale Simulations: Model real-world systems such as ecosystems or chemical interactions.

Complex Rule Sets: Explore weighted neighbor relationships for more nuanced simulations.

References

For a detailed exploration of the theoretical and experimental aspects of this project, refer to the accompanying research paper DM1_09_HexGoL_Zayimhan.pdf. This paper includes the historical context, mathematical implications, and a comparative analysis of hexagonal vs. square grid systems.

Acknowledgments

This project is inspired by Conway’s Game of Life and builds upon its principles to adapt cellular automata for hexagonal grids. Special thanks to the research contributors: Defne Demir, Hasan Saygılı, Semih Avcı, Zayimhan Korkmaz, and Zeynep Tanrıvermiş, for their comprehensive study on this topic.

License

The project and accompanying research are licensed under an open-access framework. Permission is granted for educational and research use with proper attribution.


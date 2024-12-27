import pygame
import numpy as np
import math

# Screen dimensions and hexagon parameters
WIDTH, HEIGHT = 1000, 800
HEX_SIZE = 20  # Length of a hexagon's side
BACKGROUND_COLOR = (0, 0, 0)  # Black background
BUTTON_COLOR = (100, 100, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
PAUSE_COLOR = (255, 0, 0)
SIMULATE_ACTIVE_COLOR = (0, 255, 0)  # Color of the Simulate button when active

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal Game of Life")

# Button definitions
start_button_rect = pygame.Rect(WIDTH - 300, HEIGHT - 50, 140, 40)  # Start/Pause button
simulate_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)  # Simulate button
clear_button_rect = pygame.Rect(WIDTH - 450, HEIGHT - 50, 140, 40)  # Clear button
random_button_rect = pygame.Rect(WIDTH - 600, HEIGHT - 50, 140, 40)  # Random Pattern button

# Calculate a corner of a hexagon
def hex_corner(center, i):
    angle_deg = 60 * i + 60  # Rotate 60 degrees for each corner
    angle_rad = math.pi / 180 * angle_deg
    return (center[0] + HEX_SIZE * math.cos(angle_rad),
            center[1] + HEX_SIZE * math.sin(angle_rad))

# Draw a hexagon on the screen
def draw_hexagon(x, y, is_alive):
    center = (x, y)
    points = [hex_corner(center, i) for i in range(6)]  # Calculate six corners
    color = (255, 255, 0) if is_alive else BACKGROUND_COLOR  # Yellow for alive, black for dead
    pygame.draw.polygon(screen, color, points)  # Fill the cell
    pygame.draw.polygon(screen, (0, 0, 255), points, width=1)  # Draw borders

# Define grid dimensions (rows and columns)
cols = int(WIDTH / (HEX_SIZE * 1.5))  # Horizontal spacing between columns
rows = int(HEIGHT / (HEX_SIZE * math.sqrt(3)))  # Vertical spacing between rows
grid = np.zeros((rows, cols), dtype=int)  # Initial state of the grid (all dead)

# List to store cell centers
hex_centers = []

def count_alive_cells():
    """
    Returns the total number of alive cells in the grid.
    """
    return np.sum(grid)

def draw_grid():
    global hex_centers
    hex_centers = []  # Clear the list of cell centers
    for row in range(rows):
        for col in range(cols):
            x = col * HEX_SIZE * 3 / 2  # Horizontal distance between columns
            y = row * HEX_SIZE * math.sqrt(3)  # Vertical distance between rows
            if col % 2 == 1:  # Offset odd columns by half a row
                y += HEX_SIZE * math.sqrt(3) / 2
            is_alive = grid[row][col] == 1
            draw_hexagon(x, y, is_alive)  # Draw the cell at the calculated coordinates
            hex_centers.append((x, y, row, col))  # Store the center coordinates

def draw_buttons(running_simulation, simulate_active):
    # Start/Pause button
    button_color = BUTTON_COLOR if not running_simulation else PAUSE_COLOR
    pygame.draw.rect(screen, button_color, start_button_rect)
    font = pygame.font.Font(None, 30)
    start_text = font.render("Start", True, BUTTON_TEXT_COLOR)
    screen.blit(start_text, (start_button_rect.x + 40, start_button_rect.y + 10))

    # Simulate button
    simulate_color = SIMULATE_ACTIVE_COLOR if simulate_active else BUTTON_COLOR
    pygame.draw.rect(screen, simulate_color, simulate_button_rect)
    simulate_text = font.render("Simulate", True, BUTTON_TEXT_COLOR)
    screen.blit(simulate_text, (simulate_button_rect.x + 30, simulate_button_rect.y + 10))

    # Clear button
    pygame.draw.rect(screen, BUTTON_COLOR, clear_button_rect)
    clear_text = font.render("Clear", True, BUTTON_TEXT_COLOR)
    screen.blit(clear_text, (clear_button_rect.x + 50, clear_button_rect.y + 10))

    # Random Pattern button
    pygame.draw.rect(screen, BUTTON_COLOR, random_button_rect)
    random_text = font.render("Random", True, BUTTON_TEXT_COLOR)
    screen.blit(random_text, (random_button_rect.x + 30, random_button_rect.y + 10))

def random_pattern():
    global grid
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])
    live_cells = count_alive_cells()
    dead_cells = rows * cols - live_cells
    print(f"Initial number of alive cells: {live_cells}")
    print(f"Initial number of dead cells: {dead_cells}")
    if dead_cells > 0:
        print(f"Initial Alive/Dead ratio: {live_cells / dead_cells:.2f}")
    else:
        print("All cells are alive!")

def clear_grid():
    global grid
    grid = np.zeros((rows, cols), dtype=int)

def get_neighbors(r, c):
    offsets = [(-1, 0), (0, -1), (0, +1), (+1, 0)]
    if c % 2 == 0:  # Even column
        offsets += [(-1, +1), (-1, -1)]
    else:  # Odd column
        offsets += [(+1, +1), (+1, -1)]
    neighbors = [(r + dr, c + dc) for dr, dc in offsets
                 if 0 <= r + dr < rows and 0 <= c + dc < cols]
    return neighbors

def update_grid():
    new_grid = np.copy(grid)
    for row in range(rows):
        for col in range(cols):
            live_neighbors = sum(grid[nr][nc] for nr, nc in get_neighbors(row, col))
            if grid[row][col] == 1:
                if live_neighbors in [3, 4]:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
            elif grid[row][col] == 0:
                if live_neighbors == 2:
                    new_grid[row][col] = 1
    return new_grid

def simulate_steps():
    global grid
    for _ in range(10000):  # Simulate 10,000 steps
        grid = update_grid()
    live_cells = count_alive_cells()
    dead_cells = rows * cols - live_cells
    print(f"After 10,000 iterations:")
    print(f"Number of alive cells: {live_cells}")
    print(f"Number of dead cells: {dead_cells}")
    if dead_cells > 0:
        print(f"Alive/Dead ratio: {live_cells / dead_cells:.2f}")
    else:
        print("All cells are alive!")

# Main loop
running_simulation = False
simulate_active = False
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_buttons(running_simulation, simulate_active)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mx, my):
                running_simulation = not running_simulation
            elif simulate_button_rect.collidepoint(mx, my):
                simulate_active = True
                draw_buttons(running_simulation, simulate_active)
                pygame.display.flip()
                simulate_steps()
                simulate_active = False
            elif clear_button_rect.collidepoint(mx, my):
                clear_grid()
            elif random_button_rect.collidepoint(mx, my):
                random_pattern()

    if running_simulation:
        grid = update_grid()

    clock.tick(30)

pygame.quit()

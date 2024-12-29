import pygame
import numpy as np
import math

# Ekran boyutları ve altıgen parametreleri
WIDTH, HEIGHT = 1000, 800
HEX_SIZE = 1  # Altıgenin kenar uzunluğu küçültüldü
BACKGROUND_COLOR = (0, 0, 0)  # Siyah arka plan
BUTTON_COLOR = (100, 100, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
PAUSE_COLOR = (255, 0, 0)

# Pygame başlatılıyor
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal Game of Life")

# Buton tanımlamaları
start_button_rect = pygame.Rect(WIDTH - 300, HEIGHT - 50, 140, 40)  # Başlat/Durdur butonu
next_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)   # Next Step butonu
clear_button_rect = pygame.Rect(WIDTH - 450, HEIGHT - 50, 140, 40)  # Clear butonu
random_button_rect = pygame.Rect(WIDTH - 600, HEIGHT - 50, 140, 40)  # Random Pattern butonu

# Hücrelerin durumu (satır ve sütun boyutları)
cols = 1000  # 1000 sütun
rows = 1000  # 1000 satır
grid = np.zeros((rows, cols), dtype=int)  # Hücrelerin başlangıç durumu (tümü ölü)

# Optimize edilen yüzey
hex_surface = pygame.Surface((WIDTH, HEIGHT))
hex_surface.fill(BACKGROUND_COLOR)

def draw_buttons(running_simulation):
    # Başlat/Durdur butonu
    button_color = BUTTON_COLOR if not running_simulation else PAUSE_COLOR
    button_text = "Start" if not running_simulation else "Pause"
    pygame.draw.rect(screen, button_color, start_button_rect)
    font = pygame.font.Font(None, 30)
    text = font.render(button_text, True, BUTTON_TEXT_COLOR)
    screen.blit(text, (start_button_rect.x + 30, start_button_rect.y + 10))

    # Next Step butonu
    pygame.draw.rect(screen, BUTTON_COLOR, next_button_rect)
    next_text = font.render("Next Step", True, BUTTON_TEXT_COLOR)
    screen.blit(next_text, (next_button_rect.x + 20, next_button_rect.y + 10))

    # Clear butonu
    pygame.draw.rect(screen, BUTTON_COLOR, clear_button_rect)
    clear_text = font.render("Clear", True, BUTTON_TEXT_COLOR)
    screen.blit(clear_text, (clear_button_rect.x + 50, clear_button_rect.y + 10))

    # Rastgele desen butonu
    pygame.draw.rect(screen, BUTTON_COLOR, random_button_rect)
    random_text = font.render("Random", True, BUTTON_TEXT_COLOR)
    screen.blit(random_text, (random_button_rect.x + 30, random_button_rect.y + 10))

def draw_step_counter(step_count):
    """
    Displays the step count on the screen.
    """
    font = pygame.font.Font(None, 36)
    step_text = f"Steps: {step_count}"
    text = font.render(step_text, True, BUTTON_TEXT_COLOR)
    screen.blit(text, (10, HEIGHT - 40))

def random_pattern():
    global grid
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

def clear_grid():
    global grid
    grid = np.zeros((rows, cols), dtype=int)

def update_grid():
    """
    Update the grid using numpy operations for faster processing.
    """
    global grid
    neighbor_count = sum(
        np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]
    )
    grid = ((grid == 1) & ((neighbor_count == 3) | (neighbor_count == 4))) | (
        (grid == 0) & (neighbor_count == 2)
    )
    grid = grid.astype(int)

def draw_grid():
    """
    Draw only the active cells for better performance.
    """
    hex_surface.fill(BACKGROUND_COLOR)
    live_cells = np.argwhere(grid == 1)
    for (row, col) in live_cells:
        x = col * HEX_SIZE * 3 / 2
        y = row * HEX_SIZE * math.sqrt(3)
        if col % 2 == 1:  # Offset for odd columns
            y += HEX_SIZE * math.sqrt(3) / 2
        pygame.draw.circle(hex_surface, (255, 255, 0), (int(x), int(y)), HEX_SIZE)

# Ana döngü
running_simulation = False
running = True
clock = pygame.time.Clock()
step_count = 0  # Initialize step counter
state_history = set()  # Set to track previous states

while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    screen.blit(hex_surface, (0, 0))
    draw_buttons(running_simulation)
    draw_step_counter(step_count)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if random_button_rect.collidepoint(mx, my):
                random_pattern()
                state_history.clear()
                step_count = 0
                running_simulation = True

    if running_simulation:
        grid_hash = hash(grid.tobytes())
        if grid_hash in state_history:
            print(f"Infinite loop detected at step {step_count}. Restarting...")
            random_pattern()
            state_history.clear()
            step_count = 0
        else:
            state_history.add(grid_hash)
            update_grid()
            step_count += 1

    clock.tick(30)  # Increased frame rate to 30 FPS

pygame.quit()

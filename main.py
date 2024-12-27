import pygame
import numpy as np
import math

# Ekran boyutları ve altıgen parametreleri
WIDTH, HEIGHT = 1000, 800
HEX_SIZE = 20  # Altıgenin kenar uzunluğu
BACKGROUND_COLOR = (0, 0, 0)  # Siyah arka plan
BUTTON_COLOR = (100, 100, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
PAUSE_COLOR = (255, 0, 0)

history = []  # Önceki grid durumlarını tutar

mouse_pressed = False  # Fare herhangi bir tuşa basılı mı?
mouse_button = None  # Basılı olan fare tuşu ("left" veya "right")

# Pygame başlatılıyor
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal Game of Life")

# Buton tanımlamaları
start_button_rect = pygame.Rect(WIDTH - 300, HEIGHT - 50, 140, 40)  # Başlat/Durdur butonu
next_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)   # Next Step butonu
clear_button_rect = pygame.Rect(WIDTH - 450, HEIGHT - 50, 140, 40)  # Clear butonu
random_button_rect = pygame.Rect(WIDTH - 600, HEIGHT - 50, 140, 40)  # Random Pattern butonu

# Slider tanımlamaları
slider_rect = pygame.Rect(50, 50, 300, 10)  # Slider çubuğu
slider_handle_rect = pygame.Rect(50, 40, 20, 30)  # Sürüklenebilir düğme
slider_color = (100, 100, 100)
slider_handle_color = (255, 255, 255)
simulation_speed = 5  # Varsayılan hız (fps)
dragging = False  # Slider sürükleme kontrolü

# Altıgenin bir köşesinin koordinatlarını hesaplama
def hex_corner(center, i):
    angle_deg = 60 * i + 60  # Her köşe için 60 derece döndürme
    angle_rad = math.pi / 180 * angle_deg
    return (center[0] + HEX_SIZE * math.cos(angle_rad),
            center[1] + HEX_SIZE * math.sin(angle_rad))

# Altıgeni ekrana çizme
def draw_hexagon(x, y, is_alive):
    center = (x, y)
    points = [hex_corner(center, i) for i in range(6)]  # Altı köşe noktası hesaplanır
    color = (255, 255, 0) if is_alive else BACKGROUND_COLOR  # Sarı: canlı, siyah: ölü
    pygame.draw.polygon(screen, color, points)  # Hücreyi doldur
    pygame.draw.polygon(screen, (0, 0, 255), points, width=1)  # Kenarlıklar

# Hücrelerin durumu (satır ve sütun boyutları)
cols = int(WIDTH / (HEX_SIZE * 1.5))  # Sütunlar arası mesafe
rows = int(HEIGHT / (HEX_SIZE * math.sqrt(3)))  # Satırlar arası mesafe
grid = np.zeros((rows, cols), dtype=int)  # Hücrelerin başlangıç durumu (tümü ölü)

# Hücre merkezlerini saklayan liste
hex_centers = []

def count_alive_cells():
    """
    Izgaradaki toplam canlı hücre sayısını döndürür.
    """
    return np.sum(grid)

def draw_grid():
    global hex_centers
    hex_centers = []  # Hücre merkezlerini saklamak için temizle
    for row in range(rows):
        for col in range(cols):
            x = col * HEX_SIZE * 3 / 2  # Sütunlar için yatay mesafe
            y = row * HEX_SIZE * math.sqrt(3)  # Satırlar için dikey mesafe
            if col % 2 == 1:  # Tek sütunlar bir satır kaydırılır
                y += HEX_SIZE * math.sqrt(3) / 2
            is_alive = grid[row][col] == 1
            draw_hexagon(x, y, is_alive)  # Hücreyi hesaplanan koordinatlarla çiz
            hex_centers.append((x, y, row, col))  # Merkez koordinatlarını sakla

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

def draw_slider():
    pygame.draw.rect(screen, slider_color, slider_rect)
    pygame.draw.rect(screen, slider_handle_color, slider_handle_rect)
    font = pygame.font.Font(None, 30)
    text = font.render(f"Speed: {simulation_speed}", True, (255, 255, 255))
    screen.blit(text, (slider_rect.x + slider_rect.width + 20, slider_rect.y - 10))

def handle_slider(mx, dragging):
    global simulation_speed
    if dragging and slider_rect.x <= mx <= slider_rect.x + slider_rect.width:
        slider_handle_rect.x = mx - slider_handle_rect.width // 2
        relative_position = (slider_handle_rect.x - slider_rect.x) / slider_rect.width
        simulation_speed = max(1, int(relative_position * 20)) 

def select_hex(mx, my):
    for x, y, row, col in hex_centers:
        dx = mx - x
        dy = my - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance <= HEX_SIZE:
            grid[row][col] = 1 - grid[row][col]
            break

def random_pattern():
    global grid
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])
    print(f"Başlangıçtaki canlı hücre sayısı: {count_alive_cells()}")

def clear_grid():
    global grid
    grid = np.zeros((rows, cols), dtype=int)

def get_neighbors(r, c):
    offsets = [(-1, 0), (0, -1), (0, +1), (+1, 0)]
    if c % 2 == 0:  # Çift sütun
        offsets += [(-1, +1), (-1, -1)]
    else:  # Tek sütun
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

def draw_statistics():
    font = pygame.font.Font(None, 35)
    text = font.render(f"Alive # : {count_alive_cells()}", True, (255, 255, 255))
    screen.blit(text, (40, HEIGHT - 50))

def analyze_pattern():
    """
    Grid'in evrimini analiz eder.
    - Eğer sabit bir durumdaysa: 'Stable'
    - Eğer döngüye girdiyse: 'Oscillating'
    - Eğer kaotik bir durumdaysa: 'Chaotic'
    """
    global history

    # Şimdiki grid'i geçmişe ekle
    current_grid = np.copy(grid)
    history.append(current_grid)

    # Tarih kontrolü için maksimum uzunluk sınırı koy (örneğin 100 adım)
    if len(history) > 100:
        history.pop(0)

    # Sabit durum kontrolü
    if len(history) >= 2 and np.array_equal(history[-1], history[-2]):
        return "Stable"

    # Döngü kontrolü (önceki durumların tekrarı)
    for i in range(len(history) - 1):
        if np.array_equal(history[i], current_grid):
            return "Oscillating"

    # Eğer durum sabit veya döngü değilse, kaotik olarak kabul edilir
    return "Chaotic"    

def draw_analysis_result():
    """
    Grid'in analiz sonucunu ekrana yazar.
    """
    font = pygame.font.Font(None, 35)
    result = analyze_pattern()
    result_text = font.render(f"Analysis: {result}", True, (255, 255, 255))
    screen.blit(result_text, (WIDTH - 280, 40))



# Ana döngü
running_simulation = False
show_next_step = False
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_buttons(running_simulation)
    draw_slider()
    draw_statistics()
    draw_analysis_result()
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if slider_handle_rect.collidepoint(mx, my):
                dragging = True
            elif start_button_rect.collidepoint(mx, my):
                running_simulation = not running_simulation
                if running_simulation:
                    print(f"Beginning of simulation - living grid count: {count_alive_cells()}")
            elif next_button_rect.collidepoint(mx, my):
                show_next_step = True
            elif clear_button_rect.collidepoint(mx, my):
                clear_grid()
            elif random_button_rect.collidepoint(mx, my):
                random_pattern()
            elif not running_simulation:
                select_hex(mx, my)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mx, my = pygame.mouse.get_pos()
            handle_slider(mx, dragging)

    if running_simulation or show_next_step:
        grid = update_grid()
        show_next_step = False

    clock.tick(simulation_speed)

pygame.quit() 
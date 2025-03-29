import pygame
import sys
import os
import math
from constants import *
from utils import *
from title import *
import random

def load_images():
    # --- Load background images ---
    global SETUP_BG_IMG, GAME_BG_IMG
    try:
        SETUP_BG_IMG = pygame.image.load(os.path.join("images", "setup_bg.png")).convert()
        SETUP_BG_IMG = pygame.transform.scale(SETUP_BG_IMG, (WIDTH - TOOLBAR_WIDTH, HEIGHT))
    except Exception as e:
        print("Error loading setup_bg.png:", e)
        SETUP_BG_IMG = None
    try:
        GAME_BG_IMG = pygame.image.load(os.path.join("images", "game_bg.png")).convert()
        GAME_BG_IMG = pygame.transform.scale(GAME_BG_IMG, (WIDTH - TOOLBAR_WIDTH, HEIGHT))
    except Exception as e:
        print("Error loading game_bg.png:", e)
        GAME_BG_IMG = None

    # --- Load other images ---
    global MOUNTAIN_IMG, VILLAGE_IMG, FARMLAND_IMG, CASTLE_IMG, WIN_IMG, LOSE_IMG, LASTWIN_IMG, END_IMG
    try:
        MOUNTAIN_IMG = pygame.image.load(os.path.join("images", "mountain.png")).convert_alpha()
        MOUNTAIN_IMG = pygame.transform.scale(MOUNTAIN_IMG, (TILE_SIZE, TILE_SIZE))
    except Exception as e:
        print("Error loading mountain.png:", e)
        MOUNTAIN_IMG = None
    try:
        VILLAGE_IMG = pygame.image.load(os.path.join("images", "village.png")).convert_alpha()
        VILLAGE_IMG = pygame.transform.scale(VILLAGE_IMG, (TILE_SIZE, TILE_SIZE))
    except Exception as e:
        print("Error loading village.png:", e)
        VILLAGE_IMG = None
    try:
        FARMLAND_IMG = pygame.image.load(os.path.join("images", "farmland.png")).convert_alpha()
        FARMLAND_IMG = pygame.transform.scale(FARMLAND_IMG, (TILE_SIZE, TILE_SIZE))
    except Exception as e:
        print("Error loading farmland.png:", e)
        FARMLAND_IMG = None
    try:
        CASTLE_IMG = pygame.image.load(os.path.join("images", "castle.png")).convert_alpha()
        CASTLE_IMG = pygame.transform.scale(CASTLE_IMG, (TILE_SIZE, TILE_SIZE * 7 / 8))
    except Exception as e:
        print("Error loading castle.png:", e)
        CASTLE_IMG = None
    try:
        WIN_IMG = pygame.image.load(os.path.join("images", "win.png")).convert_alpha()
        WIN_IMG.set_alpha(230) 
    except Exception as e:
        print("Error loading win.png:", e)
        WIN_IMG = None
    try:
        LOSE_IMG = pygame.image.load(os.path.join("images", "lose.png")).convert_alpha()
        LOSE_IMG.set_alpha(230) 
    except Exception as e:
        print("Error loading lose.png:", e)
        LOSE_IMG = None
    try:
        LASTWIN_IMG = pygame.image.load(os.path.join("images", "last_win.png")).convert_alpha()
        LASTWIN_IMG.set_alpha(230) 
    except Exception as e:
        print("Error loading last_win.png:", e)
        LASTWIN_IMG = None
    try:
        END_IMG = pygame.image.load(os.path.join("images", "end.png")).convert_alpha()
        END_IMG.set_alpha(230) 
    except Exception as e:
        print("Error loading end.png:", e)
        END_IMG = None

def load_sounds():
        # --- Load sounds ---
    global WATER_SOUND, WIN_SOUND, LOSE_SOUND, SOUND_CLICK, SOUND_VILLAGE, SOUND_FARMLAND, DRAW_SOUND, ERASE_SOUND, END_MUSIC
    try:
        pygame.mixer.music.load(os.path.join("sounds", "music.ogg"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Error loading background music:", e)
    try:
        WATER_SOUND = pygame.mixer.Sound(os.path.join("sounds", "water.ogg"))
    except Exception as e:
        print("Error loading water.ogg:", e)
        WATER_SOUND = None
    try:
        WIN_SOUND = pygame.mixer.Sound(os.path.join("sounds", "win.ogg"))
    except Exception as e:
        print("Error loading win.ogg:", e)
        WIN_SOUND = None
    try:
        LOSE_SOUND = pygame.mixer.Sound(os.path.join("sounds", "lose.ogg"))
        LOSE_SOUND.set_volume(0.5)
    except Exception as e:
        print("Error loading lose.ogg:", e)
        LOSE_SOUND = None
    try:
        SOUND_CLICK = pygame.mixer.Sound(os.path.join("sounds", "click.ogg"))
    except Exception as e:
        print("Error loading click.ogg:", e)
        SOUND_CLICK = None
    try:
        SOUND_VILLAGE = pygame.mixer.Sound(os.path.join("sounds", "village.ogg"))
    except Exception as e:
        print("Error loading village.ogg:", e)
        SOUND_VILLAGE = None
    try:
        SOUND_FARMLAND = pygame.mixer.Sound(os.path.join("sounds", "farmland.ogg"))
    except Exception as e:
        print("Error loading farmland.ogg:", e)
        SOUND_FARMLAND = None
    try:
        DRAW_SOUND = pygame.mixer.Sound(os.path.join("sounds", "draw.ogg"))
    except Exception as e:
        print("Error loading draw.ogg:", e)
        DRAW_SOUND = None
    try:
        ERASE_SOUND = pygame.mixer.Sound(os.path.join("sounds", "erase.ogg"))
        ERASE_SOUND.set_volume(5)
    except Exception as e:
        print("Error loading erase.ogg:", e)
        ERASE_SOUND = None
    try:
        END_MUSIC = pygame.mixer.Sound(os.path.join("sounds", "end.ogg"))
    except Exception as e:
        print("Error loading end.ogg:", e)
        END_MUSIC = None

class GameState:
    def __init__(self, level):
        self.grid = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.castle_pos = level['castle_pos']
        self.river_cells = level['river']
        # River cells act as floodgates and are not flooded.
        self.water_cells = set()
        self.flooded_cells = set()
        self.setup_phase = True
        self.simulation_running = False
        self.game_over = False
        self.win = False
        self.lastwin = False
        self.water_counter = 0
        self.saved_walls = None
        self.show_tutorial = False

        for (x, y), obs_type in level['obstacles'].items():
            self.grid[x][y].type = obs_type

        for x, y in self.river_cells:
            self.grid[x][y].type = 'river'
        px, py = self.castle_pos
        self.grid[px][py].type = 'castle'

    def reset_water(self):
        # Water starts flowing in the cells below each river tile.
        self.water_cells = set()
        self.flooded_cells = set()
        for (x, y) in self.river_cells:
            if y < GRID_SIZE:
                self.water_cells.add((x, y))
                self.flooded_cells.add((x, y))
        self.water_counter = 0

    def start_simulation(self):
        if self.setup_phase:
            self.setup_phase = False
            self.simulation_running = True
            self.reset_water()
            self.saved_walls = [[cell.wall for cell in row] for row in self.grid]

    def retry(self):
        # Clear all water cells on restart.
        self.water_cells = set()
        self.flooded_cells = set()
        self.setup_phase = True
        self.simulation_running = False
        self.game_over = False

    def reset_walls(self):
        for row in self.grid:
            for cell in row:
                if cell.type == 'empty':
                    cell.wall = None
        self.saved_walls = None

    def restore_walls(self):
        if self.saved_walls:
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    self.grid[x][y].wall = self.saved_walls[x][y]

    def check_win_conditions(self):
        farmland_ok = all(
            (x, y) in self.flooded_cells
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if self.grid[x][y].type == 'farmland'
        )
        castle_flooded = self.castle_pos in self.flooded_cells
        villages_flooded = any(
            self.grid[x][y].type == 'village'
            for (x, y) in self.flooded_cells
        )
        self.win = farmland_ok and castle_flooded and not villages_flooded
        self.game_over = True
        if self.win:
            if WIN_SOUND:
                WIN_SOUND.play()
        else:
            if LOSE_SOUND:
                LOSE_SOUND.play()

    def update_simulation(self):
        if not self.simulation_running or self.game_over:
            return
        self.water_counter += 1
        if self.water_counter % WATER_UPDATE_DELAY != 0:
            return
        new_water = set()
        game_over = False
        for (x, y) in self.water_cells:
            cell = self.grid[x][y]
            # If cell has a diagonal wall and an adjacent mountain, do not flow.
            if cell.wall == WALL_DIAGONAL_RIGHT:
                if x + 1 < GRID_SIZE and self.grid[x+1][y].type == 'mountain':
                    continue
            if cell.wall == WALL_DIAGONAL_LEFT:
                if x - 1 >= 0 and self.grid[x-1][y].type == 'mountain':
                    continue
            directions = cell.get_directions()
            for direction in directions:
                dx, dy = 0, 0
                if direction == 'down':
                    dy = 1
                elif direction == 'left':
                    dx = -1
                elif direction == 'right':
                    dx = 1
                elif direction == 'down_left':
                    dx, dy = -1, 1
                elif direction == 'down_right':
                    dx, dy = 1, 1
                nx, ny = x + dx, y + dy

                # Prevent flow through V-shaped diagonal walls
                if direction in ['down_left', 'down_right']:
                    # Check adjacent cell in the X-direction
                    check_x = x + (1 if direction == 'down_right' else -1)
                    check_y = y
                    
                    # Verify both cells form a V-shape
                    if (0 <= check_x < GRID_SIZE and 
                        self.grid[x][y].wall == (WALL_DIAGONAL_RIGHT if direction == 'down_right' else WALL_DIAGONAL_LEFT) and 
                        self.grid[check_x][check_y].wall == (WALL_DIAGONAL_LEFT if direction == 'down_right' else WALL_DIAGONAL_RIGHT)):
                        continue  # Skip this direction if V-shape detected

                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    # Existing horizontal wall check
                    if ny - 1 >= 0 and self.grid[nx][ny-1].wall == WALL_HORIZONTAL:
                        if direction in ['down_left', 'down_right']:
                            ny -= 1
                    target = self.grid[nx][ny]
                    
                    if target.type == 'mountain':
                        continue
                    if (nx, ny) in self.flooded_cells or (nx, ny) in new_water:
                        continue
                    if target.type == 'village':
                        if SOUND_VILLAGE:
                            SOUND_VILLAGE.stop()
                            SOUND_VILLAGE.play()
                        game_over = True
                    if target.type == 'farmland':
                        if SOUND_FARMLAND:
                            SOUND_FARMLAND.stop()
                            SOUND_FARMLAND.play()
                    new_water.add((nx, ny))
        self.water_cells = new_water
        self.flooded_cells.update(new_water)
        if WATER_SOUND:
            WATER_SOUND.stop()
            WATER_SOUND.play()
        if game_over or not self.water_cells:
            if not game_over:
                self.check_win_conditions()
            else:
                self.win = False
            self.simulation_running = False
            self.game_over = True

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Great Flood")
    clock = pygame.time.Clock()

    load_images()
    load_sounds()

    water_anim_timer = 0
    water_anim_frame_index = 0

    # Toolbar setup (icons only)
    tool_buttons = [
        {'rect': pygame.Rect(10, 10, 80, 80), 'type': TOOL_HORIZONTAL},
        {'rect': pygame.Rect(10, 100, 80, 80), 'type': TOOL_DIAGONAL_LEFT},
        {'rect': pygame.Rect(10, 190, 80, 80), 'type': TOOL_DIAGONAL_RIGHT},
        {'rect': pygame.Rect(10, 280, 80, 80), 'type': TOOL_ERASER}
    ]
    selected_tool = TOOL_NONE

    # Game state
    current_level = 0
    game_state = GameState(levels[current_level])
    # start_button = pygame.Rect(TOOLBAR_WIDTH + GRID_SIZE * TILE_SIZE - 120, HEIGHT - 40, 100, 30)
    game_state.show_tutorial = current_level < 5

    # Tutorial variables
    tutorial_font = pygame.font.Font(None, 28)
    tutorial_box = pygame.Rect(WIDTH//2-250, HEIGHT//2-100, 500, 200)
    ok_button = pygame.Rect(WIDTH//2-40, HEIGHT//2+50, 80, 40)

    # Wall drawing variables.
    dragging = False
    last_cell = (-1, -1)
    drag_row = None
    diag_start = None

    running = True
    while running:
        dt = clock.tick(FPS)
        water_anim_timer += dt
        if water_anim_timer >= WATER_FRAME_DURATION:
            water_anim_timer = 0
            water_anim_frame_index = (water_anim_frame_index + 1) % (len(WATER_ANIM_COLORS))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle tutorial popup first
            if game_state.show_tutorial:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ok_button.collidepoint(event.pos):
                        game_state.show_tutorial = False
                        if SOUND_CLICK:
                            SOUND_CLICK.play()
                continue  # Skip all other input processing during tutorial

            # Only process these events if NOT in tutorial
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if game_state.setup_phase:
                        game_state.reset_walls()
                    game_state.retry()
                elif event.key == pygame.K_SPACE:
                    if game_state.setup_phase:
                        if SOUND_CLICK:
                            SOUND_CLICK.play()
                        game_state.start_simulation()
                elif event.key == pygame.K_n and game_state.game_over:
                    if game_state.lastwin:
                        pygame.mixer.music.stop()
                        pygame.mixer.stop()
                        if END_MUSIC:
                            END_MUSIC.play()
                        pygame.event.clear()

                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            screen.fill(BLACK)
                            screen.blit(END_IMG, (0, 0))
                            pygame.display.flip()
                    else:
                        current_level = (current_level + 1) % len(levels)
                        game_state = GameState(levels[current_level])
                        # Show tutorial for first 5 levels
                        game_state.show_tutorial = current_level < 5
            
            if game_state.game_over:
                continue
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                tool_clicked = False
                for btn in tool_buttons:
                    if btn['rect'].collidepoint(x, y):
                        selected_tool = btn['type']
                        tool_clicked = True
                        if SOUND_CLICK:
                            SOUND_CLICK.play()
                        break
                if not tool_clicked:
                    if game_state.setup_phase and x > TOOLBAR_WIDTH:
                        dragging = True
                        gx = (x - TOOLBAR_WIDTH) // TILE_SIZE
                        gy = min(y // TILE_SIZE, GRID_SIZE - 1)
                        if selected_tool in (TOOL_DIAGONAL_LEFT, TOOL_DIAGONAL_RIGHT):
                            diag_start = (gx, gy)
                        elif selected_tool != TOOL_ERASER:
                            drag_row = gy
                        if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                            cell = game_state.grid[gx][gy]
                            if cell.type == 'empty':
                                if selected_tool == TOOL_ERASER:
                                    cell.wall = None
                                    ERASE_SOUND.play()
                                else:
                                    cell.wall = selected_tool
                                    DRAW_SOUND.play()
                                last_cell = (gx, gy)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                last_cell = (-1, -1)
                drag_row = None
                diag_start = None
            
            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = event.pos
                if x > TOOLBAR_WIDTH:
                    current_gx = (x - TOOLBAR_WIDTH) // TILE_SIZE
                    if selected_tool == TOOL_ERASER:
                        gx = current_gx
                        gy = min(y // TILE_SIZE, GRID_SIZE - 1)
                    elif selected_tool in (TOOL_DIAGONAL_LEFT, TOOL_DIAGONAL_RIGHT) and diag_start is not None:
                        gx = current_gx
                        if selected_tool == TOOL_DIAGONAL_LEFT:
                            gy = diag_start[1] - (gx - diag_start[0])
                        elif selected_tool == TOOL_DIAGONAL_RIGHT:
                            gy = diag_start[1] + (gx - diag_start[0])
                        gy = min(gy, GRID_SIZE - 1)
                    else:
                        gx = current_gx
                        gy = min(drag_row if drag_row is not None else (y // TILE_SIZE), GRID_SIZE - 1)
                    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                        if (gx, gy) != last_cell:
                            cell = game_state.grid[gx][gy]
                            if cell.type == 'empty':
                                if selected_tool == TOOL_ERASER:
                                    cell.wall = None
                                    ERASE_SOUND.play()
                                else:
                                    cell.wall = selected_tool
                                    DRAW_SOUND.play()
                                last_cell = (gx, gy)
        
        if game_state.simulation_running:
            game_state.update_simulation()
        
        # Draw overall background.
        if game_state.setup_phase:
            if SETUP_BG_IMG:
                screen.blit(SETUP_BG_IMG, (TOOLBAR_WIDTH, 0))
            else:
                pygame.draw.rect(screen, SETUP_BG_COLOR, (TOOLBAR_WIDTH, 0, WIDTH - TOOLBAR_WIDTH, HEIGHT))
        else:
            if GAME_BG_IMG:
                screen.blit(GAME_BG_IMG, (TOOLBAR_WIDTH, 0))
            else:
                pygame.draw.rect(screen, GAME_BG_COLOR, (TOOLBAR_WIDTH, 0, WIDTH - TOOLBAR_WIDTH, HEIGHT))
        
        # Draw toolbar.
        pygame.draw.rect(screen, TOOLBAR_COLOR, (0, 0, TOOLBAR_WIDTH, HEIGHT))
        for btn in tool_buttons:
            color = TOOL_ACTIVE_COLOR if selected_tool == btn['type'] else TOOL_COLOR
            pygame.draw.rect(screen, color, btn['rect'])
            if btn['type'] == TOOL_HORIZONTAL:
                pygame.draw.line(screen, BLACK,
                    (btn['rect'].left + 10, btn['rect'].centery),
                    (btn['rect'].right - 10, btn['rect'].centery), 3)
            elif btn['type'] == TOOL_DIAGONAL_LEFT:
                pygame.draw.line(screen, BLACK,
                    (btn['rect'].left + 10, btn['rect'].bottom - 10),
                    (btn['rect'].right - 10, btn['rect'].top + 10), 3)
            elif btn['type'] == TOOL_DIAGONAL_RIGHT:
                pygame.draw.line(screen, BLACK,
                    (btn['rect'].left + 10, btn['rect'].top + 10),
                    (btn['rect'].right - 10, btn['rect'].bottom - 10), 3)
            elif btn['type'] == TOOL_ERASER:
                r = btn['rect']

                # Define eraser parts
                eraser_width = r.width * 0.6  # Keep the same width
                eraser_height = r.height * 0.6  # Make it thinner in height

                eraser_body = pygame.Rect(
                    r.centerx - eraser_width // 2,  # Center horizontally
                    r.centery - eraser_height // 2,  # Center vertically
                    eraser_width, eraser_height
                )
                
                eraser_tip = pygame.Rect(
                    eraser_body.left, eraser_body.top, 
                    eraser_body.width * 0.3, eraser_body.height
                )

                # Draw the eraser body (blue casing)
                pygame.draw.rect(screen, (50, 100, 200), eraser_body)  # Blue case
                pygame.draw.rect(screen, (255, 255, 255), eraser_tip)  # White eraser tip

                # Outline for better visibility
                pygame.draw.rect(screen, BLACK, eraser_body, 2)
                pygame.draw.rect(screen, BLACK, eraser_tip, 2)


        
        # Draw game grid and cells.
        if game_state.setup_phase:
            wall_color = DARK_BROWN
            wall_line_width = 3
        else:
            wall_color = GREY
            wall_line_width = 5
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                cell = game_state.grid[x][y]
                rect = pygame.Rect(TOOLBAR_WIDTH + x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell.type == 'empty':
                    pass
                elif cell.type == 'mountain' and MOUNTAIN_IMG:
                    screen.blit(MOUNTAIN_IMG, rect)
                elif cell.type == 'village' and VILLAGE_IMG:
                    screen.blit(VILLAGE_IMG, rect)
                elif cell.type == 'farmland' and FARMLAND_IMG:
                    screen.blit(FARMLAND_IMG, rect)
                    if (x, y) in game_state.flooded_cells:
                        overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        overlay.fill((34, 139, 34, 150))
                        screen.blit(overlay, rect)
                elif cell.type == 'river' and game_state.setup_phase:
                    pygame.draw.rect(screen, RIVER_COLOR, rect)
                elif cell.type == 'castle' and CASTLE_IMG:
                    screen.blit(CASTLE_IMG, rect)
                if cell.wall == WALL_HORIZONTAL:
                    pygame.draw.line(screen, wall_color,
                                     (rect.left, rect.bottom - 2),
                                     (rect.right, rect.bottom - 2),
                                     wall_line_width)
                elif cell.wall == WALL_DIAGONAL_LEFT:
                    start_point = (rect.left, rect.bottom)
                    end_point = (rect.right, rect.top)
                    draw_thick_diagonal(screen, wall_color, start_point, end_point, wall_line_width)
                elif cell.wall == WALL_DIAGONAL_RIGHT:
                    start_point = (rect.left, rect.top)
                    end_point = (rect.right, rect.bottom)
                    draw_thick_diagonal(screen, wall_color, start_point, end_point, wall_line_width)
        
        # --- Draw water overlays ---
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) in game_state.flooded_cells:
                    tile_rect = pygame.Rect(TOOLBAR_WIDTH + x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    water_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    cell = game_state.grid[x][y]
                    # Full-tile water (no wall)
                    if cell.wall is None:
                        water_surf.fill(WATER_ANIM_COLORS[water_anim_frame_index])
                    elif cell.wall == WALL_HORIZONTAL:
                        clip_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE - WALL_THICKNESS)
                        pygame.draw.rect(water_surf, WATER_ANIM_COLORS[water_anim_frame_index], clip_rect)
                    elif cell.wall == WALL_DIAGONAL_RIGHT:
                        # Fill the above triangle of the cell.
                        poly = [(0, 0), (TILE_SIZE, 0), (TILE_SIZE, TILE_SIZE)]
                        pygame.draw.polygon(water_surf, WATER_ANIM_COLORS[water_anim_frame_index], poly)
                    elif cell.wall == WALL_DIAGONAL_LEFT:
                        poly = [(0, 0), (TILE_SIZE, 0), (0, TILE_SIZE)]
                        pygame.draw.polygon(water_surf, WATER_ANIM_COLORS[water_anim_frame_index], poly)
                    screen.blit(water_surf, tile_rect)
        
        # Extra water overlay for diagonal walls in adjacent cells
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                cell = game_state.grid[x][y]
                if (x, y) in game_state.flooded_cells and cell.wall in (WALL_DIAGONAL_RIGHT, WALL_DIAGONAL_LEFT):
                    if cell.wall == WALL_DIAGONAL_RIGHT and x + 1 < GRID_SIZE:
                        adj_cell = game_state.grid[x + 1][y]
                        adj_flooded = (x + 1, y) in game_state.flooded_cells
                        # Only draw overlay if adjacent cell isn't forming a V-shape
                        if not adj_flooded or (adj_flooded and adj_cell.wall == WALL_DIAGONAL_RIGHT):
                            adj_rect = pygame.Rect(TOOLBAR_WIDTH + (x + 1) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                            extra_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            poly = [(0, TILE_SIZE), (0, 0), (TILE_SIZE, TILE_SIZE)]
                            pygame.draw.polygon(extra_surf, WATER_ANIM_COLORS[water_anim_frame_index], poly)
                            screen.blit(extra_surf, adj_rect)
                    elif cell.wall == WALL_DIAGONAL_LEFT and x - 1 >= 0:
                        adj_cell = game_state.grid[x - 1][y]
                        adj_flooded = (x - 1, y) in game_state.flooded_cells
                        # Only draw overlay if adjacent cell isn't forming a V-shape
                        if not adj_flooded or (adj_flooded and adj_cell.wall == WALL_DIAGONAL_LEFT):
                            adj_rect = pygame.Rect(TOOLBAR_WIDTH + (x - 1) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                            extra_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            poly = [(TILE_SIZE, TILE_SIZE), (TILE_SIZE, 0), (0, TILE_SIZE)]
                            pygame.draw.polygon(extra_surf, WATER_ANIM_COLORS[water_anim_frame_index], poly)
                            screen.blit(extra_surf, adj_rect)
        
        # Draw grid lines in setup mode.
        if game_state.setup_phase:
            for x in range(GRID_SIZE + 1):
                start_line = (TOOLBAR_WIDTH + x * TILE_SIZE, 0)
                end_line = (TOOLBAR_WIDTH + x * TILE_SIZE, HEIGHT)
                pygame.draw.line(screen, DARK_BROWN, start_line, end_line, 1)
            for y in range(GRID_SIZE + 1):
                start_line = (TOOLBAR_WIDTH, y * TILE_SIZE)
                end_line = (WIDTH, y * TILE_SIZE)
                pygame.draw.line(screen, DARK_BROWN, start_line, end_line, 1)
        
        # Draw centered win/lose message.
        # Calculate game area dimensions (excluding toolbar)
        game_screen_width = GRID_SIZE * TILE_SIZE
        game_screen_height = HEIGHT

        # Calculate the center of the game screen (excluding the toolbar)
        center_x = TOOLBAR_WIDTH + game_screen_width / 2
        center_y = game_screen_height / 2

        if game_state.game_over:
            if game_state.win:
                img_width = WIN_IMG.get_width()
                img_height = WIN_IMG.get_height()

                # Calculate position to center the image in the game area (excluding toolbar)
                image_x = TOOLBAR_WIDTH + (game_screen_width - img_width) / 2
                image_y = (game_screen_height - img_height) / 2
                
                if current_level == 12:
                    screen.blit(LASTWIN_IMG, (image_x, image_y))
                    game_state.lastwin = True
                else:
                    screen.blit(WIN_IMG, (image_x, image_y))

                # Overlay stats text in green over the win image.
                if current_level > 4:
                    stats_font = pygame.font.Font(None, 36)
                    green_color = (0, 180, 0)
                    villages_saved = villageCount[current_level - 5]
                    fields_irrigated = fieldCount[current_level - 5]
                    villages_text = f"Villages Saved: {villages_saved}"
                    fields_text = f"Fields Irrigated: {fields_irrigated}"
                    villages_surface = stats_font.render(villages_text, True, green_color)
                    fields_surface = stats_font.render(fields_text, True, green_color)
                    villages_rect = villages_surface.get_rect(center=(center_x - 105, image_y + img_height/2))
                    fields_rect = fields_surface.get_rect(center=(center_x - 100, image_y + img_height/2 + 40))
                    screen.blit(villages_surface, villages_rect)
                    screen.blit(fields_surface, fields_rect)

            else:
                img_width = LOSE_IMG.get_width()
                img_height = LOSE_IMG.get_height()

                image_x = TOOLBAR_WIDTH + (game_screen_width - img_width) / 2
                image_y = (game_screen_height - img_height) / 2
                
                screen.blit(LOSE_IMG, (image_x, image_y))
        
        # Draw tutorial popup
        if game_state.show_tutorial:
            # Transparent overlay
            overlay = pygame.Surface((500, 200), pygame.SRCALPHA)
            overlay.fill((255, 255, 220, 220))
            screen.blit(overlay, tutorial_box.topleft)
            
            # Border
            pygame.draw.rect(screen, DARK_BROWN, tutorial_box, 3)
            
            # Text
            lines = TUTORIAL_MESSAGES[current_level].split('\n')
            y_pos = tutorial_box.top + 20
            for line in lines:
                text = tutorial_font.render(line.strip(), True, BLACK)
                screen.blit(text, (tutorial_box.centerx - text.get_width()/2, y_pos))
                y_pos += 30
            
            # OK button
            btn_color = BUTTON_ACTIVE_COLOR if ok_button.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(screen, btn_color, ok_button)
            pygame.draw.rect(screen, DARK_BROWN, ok_button, 2)
            ok_text = tutorial_font.render("OK", True, BLACK)
            screen.blit(ok_text, ok_text.get_rect(center=ok_button.center))

        # Draw level counter.
        if current_level < 5:
            level_text = pygame.font.Font(None, 24).render(f"Tutorial Level {current_level + 1}", True, BLACK)
        else:
            level_text = pygame.font.Font(None, 24).render(f"Level {current_level - 4}", True, BLACK)
        screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
        
        pygame.display.flip()

if __name__ == "__main__":
    # Initialize pygame and mixer.
    pygame.init()
    pygame.mixer.init()
    title_screen()
    main()

import pygame
import os
import sys
import random
from constants import *

# Global Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
FPS = 60
RIVER_SPEED = 3  # pixels per update

# Title river colors and corresponding thickness:
# Whitest (249,237,188) is thickest, darkest (226,196,137) is thinnest,
# and the middle (229,205,154) is in between.
TITLE_RIVER_COLORS = [(249, 237, 188), (226, 196, 137), (229, 205, 154)]
COLOR_THICKNESS = {
    (249, 237, 188): 4,
    (229, 205, 154): 3,
    (226, 196, 137): 2
}

def generate_river():
    """
    Generate a new river configuration.
    The river spawns on one side of the screen and grows until it covers
    the full screen in that direction, then fades away from the same side.
    """
    river = {}
    river['orientation'] = random.choice(["horizontal", "vertical"])
    river['color'] = random.choice(TITLE_RIVER_COLORS)
    river['thickness'] = COLOR_THICKNESS[river['color']]
    river['speed'] = RIVER_SPEED
    # These variables control the "growing" then "fading" phases.
    river['current_length'] = 0   # how much of the river is visible
    river['fade_offset'] = 0      # how much of the beginning has faded away
    river['phase'] = "growing"    # phases: "growing" then "fading"
    
    if river['orientation'] == "horizontal":
        river['direction'] = random.choice(["left_to_right", "right_to_left"])
        river['y'] = random.randint(0, SCREEN_HEIGHT)
        # For horizontal rivers, the full length is the screen width.
        river['max_length'] = SCREEN_WIDTH
        if river['direction'] == "left_to_right":
            river['start_x'] = 0
            river['dx'] = RIVER_SPEED
        else:
            river['start_x'] = SCREEN_WIDTH
            river['dx'] = -RIVER_SPEED
    else:
        river['direction'] = random.choice(["top_to_bottom", "bottom_to_top"])
        river['x'] = random.randint(0, SCREEN_WIDTH)
        # For vertical rivers, the full length is the screen height.
        river['max_length'] = SCREEN_HEIGHT
        if river['direction'] == "top_to_bottom":
            river['start_y'] = 0
            river['dy'] = RIVER_SPEED
        else:
            river['start_y'] = SCREEN_HEIGHT
            river['dy'] = -RIVER_SPEED
    return river

def update_river(river):
    """Update the river's growth and fading based on its phase."""
    if river['orientation'] == "horizontal":
        if river['phase'] == "growing":
            river['current_length'] += river['speed']
            if river['current_length'] >= river['max_length']:
                river['current_length'] = river['max_length']
                river['phase'] = "fading"
        elif river['phase'] == "fading":
            river['fade_offset'] += river['speed']
            if river['fade_offset'] >= river['max_length']:
                river['phase'] = "finished"
    else:  # vertical
        if river['phase'] == "growing":
            river['current_length'] += river['speed']
            if river['current_length'] >= river['max_length']:
                river['current_length'] = river['max_length']
                river['phase'] = "fading"
        elif river['phase'] == "fading":
            river['fade_offset'] += river['speed']
            if river['fade_offset'] >= river['max_length']:
                river['phase'] = "finished"

def draw_river(screen, river):
    """Draw the growing/fading river as a line on the screen."""
    if river['phase'] == "finished":
        return

    color = river['color']
    thickness = river['thickness']
    if river['orientation'] == "horizontal":
        # For horizontal, the river spans from the start_x offset by fade_offset
        # to start_x offset by current_length.
        if river['direction'] == "left_to_right":
            start_pos = (int(river['start_x'] + river['fade_offset']), int(river['y']))
            end_pos = (int(river['start_x'] + river['current_length']), int(river['y']))
        else:  # right_to_left
            start_pos = (int(river['start_x'] - river['current_length']), int(river['y']))
            end_pos = (int(river['start_x'] - river['fade_offset']), int(river['y']))
    else:
        # For vertical, similar idea along the y axis.
        if river['direction'] == "top_to_bottom":
            start_pos = (int(river['x']), int(river['start_y'] + river['fade_offset']))
            end_pos = (int(river['x']), int(river['start_y'] + river['current_length']))
        else:  # bottom_to_top
            start_pos = (int(river['x']), int(river['start_y'] - river['current_length']))
            end_pos = (int(river['x']), int(river['start_y'] - river['fade_offset']))
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)

def is_river_finished(river):
    """Check if the river's animation is complete."""
    return river.get('phase', '') == "finished"

def title_screen():
    """Display the title screen with animated rivers, a calligraphy title, and a Start button."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Great Flood")
    clock = pygame.time.Clock()
    
    # Load background image.
    try:
        TITLE_BG_IMG = pygame.image.load(os.path.join("images", "title_bg.png")).convert()
        TITLE_BG_IMG = pygame.transform.scale(TITLE_BG_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print("Error loading title_bg.png:", e)
        TITLE_BG_IMG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        TITLE_BG_IMG.fill((30, 30, 30))
    
    # Load sounds.
    try:
        DAM_SOUND = pygame.mixer.Sound(os.path.join("sounds", "dam.ogg"))
        DAM_SOUND.set_volume(0.8)
        DAM_SOUND.play(loops=-1)
    except Exception as e:
        print("Error loading dam.ogg:", e)
        DAM_SOUND = None
    try:
        AMBIENCE_SOUND = pygame.mixer.Sound(os.path.join("sounds", "ambience.ogg"))
        AMBIENCE_SOUND.set_volume(1)
        AMBIENCE_SOUND.play(loops=-1)
    except Exception as e:
        print("Error loading ambience.ogg:", e)
        AMBIENCE_SOUND = None
    try:
        SOUND_CLICK = pygame.mixer.Sound(os.path.join("sounds", "click.ogg"))
    except Exception as e:
        print("Error loading click.ogg:", e)
        SOUND_CLICK = None

    # Fonts
    font = pygame.font.Font(None, 36)
    # Attempt to load a calligraphy-style font.
    # Try "Brush Script MT" first, then "Lucida Calligraphy".
    calligraphy_font_name = pygame.font.match_font("brushscriptmt") or pygame.font.match_font("lucidacalligraphy")
    if calligraphy_font_name:
        title_font = pygame.font.Font(calligraphy_font_name, 72)
    else:
        title_font = pygame.font.Font(None, 72)
    
    # Position title and button closer to center.
    title_text = title_font.render("The Great Flood", True, (1, 3, 0))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    padding = 10
    title_box_rect = pygame.Rect(
        title_rect.left - padding,
        title_rect.top - padding,
        title_rect.width + 2 * padding,
        title_rect.height + 2 * padding
    )
    
    start_button_rect = pygame.Rect(0, 0, 150, 50)
    start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
    base_button_color = (173, 77, 36)
    hover_button_color = (156, 69, 32)
    
    # Manage rivers.
    rivers = []
    MIN_RIVERS = 3
    ADD_RIVER_INTERVAL = 800  # milliseconds between new river spawns.
    last_river_add = pygame.time.get_ticks()
    
    running = True
    while running:
        dt = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        button_hover = start_button_rect.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    if SOUND_CLICK:
                        SOUND_CLICK.play()
                    running = False
        
        # Update rivers.
        for river in rivers:
            update_river(river)
        # Remove finished rivers.
        rivers = [river for river in rivers if not is_river_finished(river)]
        # Spawn new rivers if there are too few or enough time has passed.
        current_time = pygame.time.get_ticks()
        if len(rivers) < MIN_RIVERS or (current_time - last_river_add >= ADD_RIVER_INTERVAL):
            rivers.append(generate_river())
            last_river_add = current_time
        
        # Draw background.
        screen.blit(TITLE_BG_IMG, (0, 0))
        # Draw all rivers.
        for river in rivers:
            draw_river(screen, river)
        
        # Draw title text box and title.
        pygame.draw.rect(screen, (255, 242, 217), title_box_rect)
        screen.blit(title_text, title_rect)
        
        # Draw the Start button with hover effect.
        btn_color = hover_button_color if button_hover else base_button_color
        pygame.draw.rect(screen, btn_color, start_button_rect)
        pygame.draw.rect(screen, (200, 200, 200), start_button_rect, 2)
        start_text = font.render("Start", True, (253, 244, 218))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)
        
        pygame.display.flip()
    
    if DAM_SOUND:
        DAM_SOUND.stop()
    if AMBIENCE_SOUND:
        AMBIENCE_SOUND.stop()
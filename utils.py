import pygame
import math
from constants import *

def draw_thick_diagonal(surface, color, start, end, thickness):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    offset_x = -dy / length * thickness / 2
    offset_y = dx / length * thickness / 2
    points = [
        (start[0] + offset_x, start[1] + offset_y),
        (start[0] - offset_x, start[1] - offset_y),
        (end[0] - offset_x, end[1] - offset_y),
        (end[0] + offset_x, end[1] + offset_y)
    ]
    pygame.draw.polygon(surface, color, points)

class Cell:
    def __init__(self, cell_type='empty', wall=None):
        self.type = cell_type
        self.wall = wall

    def get_directions(self):
        if self.wall == WALL_HORIZONTAL:
            return ['left', 'right']
        elif self.wall == WALL_DIAGONAL_LEFT:
            return ['down_left']
        elif self.wall == WALL_DIAGONAL_RIGHT:
            return ['down_right']
        return ['down']
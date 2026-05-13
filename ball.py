import pygame
import sys
import math
import random
import json
import os
from collections import defaultdict
from shapely.geometry import Point, Polygon

# Load config
WIDTH, HEIGHT = 1000, 800
BG_IMAGE_PATH = 'map_bg.png'
SHAPES = []
POLYGONS = []
TOTAL_BALLS = 500

if os.path.exists('game_config.json'):
    with open('game_config.json', 'r') as f:
        config = json.load(f)
        SHAPES = config.get('shapes', [])
        BG_IMAGE_PATH = config.get('bg_path', 'map_bg.png')
        TOTAL_BALLS = config.get('ball_count', 1000)
        # Pre-create Shapely polygons for performance
        for s in SHAPES:
            # if len(s) >= 3:
                POLYGONS.append(Polygon(s))

# Constants
CELL_SIZE = 25
BALL_RADIUS = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crowd Visualizer - Madrid")
clock = pygame.time.Clock()

# Load Assets
if os.path.exists(BG_IMAGE_PATH):
    BG_IMAGE = pygame.image.load(BG_IMAGE_PATH).convert()
else:
    BG_IMAGE = None

def check_dot_in_shapes(x, y):
    """
    Checks if a dot is inside any shape using Shapely.
    """
    p = Point(x, y)
    for poly in POLYGONS:
        if poly.contains(p):
            return True
    return False

class Ball:
    __slots__ = ['pos', 'velocity', 'color', 'radius']
    def __init__(self, x, y):
        self.pos = [float(x), float(y)]
        self.radius = BALL_RADIUS
        self.velocity = [random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)]
        self.color = random.choice([
            (255, 200, 150), (200, 150, 100), (100, 100, 255), (255, 100, 100), (100, 255, 100)
        ])

    def update(self):
        old_pos = list(self.pos)
        
        # 1. Move
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # 2. Collision with Polygons (The "Shapes" list)
        if check_dot_in_shapes(self.pos[0], self.pos[1]):
            self.pos = old_pos
            self.velocity[0] *= -0.5
            self.velocity[1] *= -0.5

        # 3. Decay/Friction
        self.velocity[0] *= 0.98
        self.velocity[1] *= 0.98

        # 4. Wall Collisions
        if self.pos[0] < self.radius or self.pos[0] > WIDTH - self.radius:
            self.velocity[0] *= -1
        if self.pos[1] < self.radius or self.pos[1] > HEIGHT - self.radius:
            self.velocity[1] *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

def handle_repulsions(balls):
    grid = defaultdict(list)
    for b in balls:
        cx, cy = int(b.pos[0] // CELL_SIZE), int(b.pos[1] // CELL_SIZE)
        grid[(cx, cy)].append(b)
    
    for (cx, cy), cell_balls in grid.items():
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_key = (cx + dx, cy + dy)
                if neighbor_key in grid:
                    for b1 in cell_balls:
                        for b2 in grid[neighbor_key]:
                            if b1 is b2: continue
                            dx_p, dy_p = b1.pos[0] - b2.pos[0], b1.pos[1] - b2.pos[1]
                            dist_sq = dx_p**2 + dy_p**2
                            min_d = b1.radius + b2.radius + 2
                            if dist_sq < min_d**2:
                                dist = math.sqrt(dist_sq) or 0.1
                                overlap = min_d - dist
                                b1.velocity[0] += (dx_p / dist) * overlap * 0.1
                                b1.velocity[1] += (dy_p / dist) * overlap * 0.1

active_balls = []
spawn_point = [WIDTH // 2, HEIGHT // 2]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            spawn_point = list(event.pos)

    if len(active_balls) < TOTAL_BALLS:
        active_balls.append(Ball(spawn_point[0], spawn_point[1]))

    handle_repulsions(active_balls)
    for ball in active_balls:
        ball.update()

    if BG_IMAGE:
        screen.blit(BG_IMAGE, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # Draw the SHAPES list
    shape_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for shape in SHAPES:
        # if len(shape) > 2:
            pygame.draw.polygon(shape_surf, (0, 0, 0, 100), shape)
            pygame.draw.polygon(shape_surf, (255, 255, 255, 150), shape, 1)
    screen.blit(shape_surf, (0, 0))

    for ball in active_balls:
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

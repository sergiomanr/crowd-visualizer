import pygame
import sys
import math
import random
from collections import defaultdict
from shapely.geometry import Point, Polygon

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 35  # Slightly larger than ball diameter
BALL_RADIUS = 5
all_black_shapes = [
    [(500, 300), (500, 330), (600, 330), (600, 300)]]

# Get total number of balls from command line or default to 100
total_balls = 100
if len(sys.argv) > 1:
    try:
        total_balls = int(sys.argv[1])
    except ValueError:
        print(f"Invalid number of balls: {sys.argv[1]}. Using default of 100.")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Optimized Repelling Balls ({total_balls})")
clock = pygame.time.Clock()

def check_dot_in_shapes(dot_coords, list_of_shapes):
    """
    Checks if a dot is inside any shape from a list using Shapely.
    """
    point = Point(dot_coords)
    for shape_points in list_of_shapes:
        polygon = Polygon(shape_points)
        if polygon.contains(point):
            return True
    return False

class Ball:
    __slots__ = ['pos', 'velocity', 'color', 'radius']
    def __init__(self, x, y):
        self.pos = [float(x), float(y)]
        self.radius = BALL_RADIUS
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def update(self):
        # 1. Move
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # 2. Logarithmic Decay
        mag_sq = self.velocity[0]**2 + self.velocity[1]**2
        if mag_sq > 0.0001:
            magnitude = math.sqrt(mag_sq)
            decay = 0.99 * math.log1p(magnitude)
            new_mag = max(0, magnitude - decay) * 0.99
            ratio = new_mag / magnitude
            self.velocity[0] *= ratio
            self.velocity[1] *= ratio
        else:
            self.velocity = [0.0, 0.0]

        # 3. Wall Collisions
        if self.pos[0] < self.radius:
            self.pos[0] = self.radius
            self.velocity[0] = abs(self.velocity[0])
        elif self.pos[0] > WIDTH - self.radius:
            self.pos[0] = WIDTH - self.radius
            self.velocity[0] = -abs(self.velocity[0])

        if self.pos[1] < self.radius:
            self.pos[1] = self.radius
            self.velocity[1] = abs(self.velocity[1])
        elif self.pos[1] > HEIGHT - self.radius:
            self.pos[1] = HEIGHT - self.radius
            self.velocity[1] = -abs(self.velocity[1])
        if self.pos[0] > 500 and self.pos[1] > 300:
            # print((self.pos[0],self.pos[1]))
            if check_dot_in_shapes((self.pos[0]+0.5*self.radius,self.pos[1]+0.5*self.radius),all_black_shapes):
                self.pos[0] -= self.radius
                self.pos[1] -= self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

# Static Obstacle Constants
BOX_X, BOX_Y = 500, 300
BOX_SIDE = 30

def handle_repulsions_grid(balls):
    # Spatial Partitioning: Grid
    grid = defaultdict(list)
    for b in balls:
        cx = int(b.pos[0] // CELL_SIZE)
        cy = int(b.pos[1] // CELL_SIZE)
        grid[(cx, cy)].append(b)
    
    for (cx, cy), cell_balls in grid.items():
        # --- Ball-Box Repulsion ---
        # Grid cells for Box(500, 300) with CELL_SIZE=35 are (14, 8)
        if abs(cx - 14) <= 1 and abs(cy - 8) <= 1:
            bx, by = BOX_X + BOX_SIDE/2, BOX_Y + BOX_SIDE/2
            for b1 in cell_balls:
                dx = b1.pos[0] - bx
                dy = b1.pos[1] - by
                dist_sq = dx**2 + dy**2
                min_dist = b1.radius + BOX_SIDE/2
                if dist_sq < min_dist**2:
                    dist = math.sqrt(dist_sq) or 0.1
                    overlap = min_dist - dist
                    b1.velocity[0] += (dx / dist) * overlap * 0.5
                    b1.velocity[1] += (dy / dist) * overlap * 0.5

        # Ball-Ball Repulsion
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_key = (cx + dx, cy + dy)
                if neighbor_key in grid:
                    for b1 in cell_balls:
                        for b2 in grid[neighbor_key]:
                            if b1 is b2: continue
                            dx_p = b1.pos[0] - b2.pos[0]
                            dy_p = b1.pos[1] - b2.pos[1]
                            dist_sq = dx_p**2 + dy_p**2
                            min_d = b1.radius + b2.radius
                            if dist_sq < min_d**2:
                                dist = math.sqrt(dist_sq) or 0.1
                                overlap = min_d - dist
                                nx, ny = dx_p / dist, dy_p / dist
                                push = 0.1
                                b1.velocity[0] += nx * overlap * push
                                b1.velocity[1] += ny * overlap * push
                                b2.velocity[0] -= nx * overlap * push
                                b2.velocity[1] -= ny * overlap * push

active_balls = []
balls_spawned = 0
spawn_per_frame = max(1, total_balls // 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Spawning
    for _ in range(spawn_per_frame):
        if balls_spawned < total_balls:
            active_balls.append(Ball(WIDTH // 2, HEIGHT // 2))
            balls_spawned += 1

    # Physics
    handle_repulsions_grid(active_balls)
    for ball in active_balls:
        ball.update()

    # Drawing
    screen.fill((30, 30, 30))
    pygame.draw.polygon(screen, (0, 0, 0), all_black_shapes[0])
    # Render Box
    # Render Balls
    for ball in active_balls:
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

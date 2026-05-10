import pygame
import sys
from shapely.geometry import Point, Polygon

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

# --- Data ---
red_dot = (500, 300)
all_black_shapes = [
    [(10, 10), (10, 100), (100, 100), (100, 10)],
    [(200, 200), (200, 300), (300, 300), (300, 200)]
]

# --- Calculation ---
result = check_dot_in_shapes(red_dot, all_black_shapes)
print(f"Is the red dot inside a black shape? {result}")

# --- Visualization ---
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shape Visualization")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background (white)
    screen.fill((200, 200, 200))

    # Draw black shapes
    for shape in all_black_shapes:
        # pygame.draw.polygon takes a list of (x, y) tuples
        pygame.draw.polygon(screen, (0, 0, 0), shape)
        # Draw outline to make them clearer
        pygame.draw.polygon(screen, (50, 50, 50), shape, 2)

    # Draw red dot
    pygame.draw.circle(screen, (255, 0, 0), red_dot, 5)

    pygame.display.flip()

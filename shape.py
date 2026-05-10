import pygame
import sys
from shapely.geometry import Point, Polygon
import numpy as np
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
all_black_shapes = []

# --- Calculation ---
# result = check_dot_in_shapes(red_dot, all_black_shapes)
# print(f"Is the red dot inside a black shape? {result}")
import cv2
def get_black_shapes_coordinates(image_path):
    """
    Reads a black and white image and returns a list of lists containing 
    the (x, y) coordinates of the boundaries of all black shapes.
    """
    # 1. Load the image in Grayscale
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray_image is None:
        print("Error: Could not load the image. Check the file path.")
        return []

    # 2. Convert to strict Binary and Invert
    # cv2.THRESH_BINARY_INV turns Black pixels to White (255) and White to Black (0).
    # This is required because findContours looks for white shapes.
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

    # 3. Find the contours (the boundaries of the shapes)
    # RETR_EXTERNAL extracts only the outer boundaries of the shapes.
    # CHAIN_APPROX_SIMPLE compresses straight lines (e.g., a straight wall 
    # will just be 2 corner points instead of 100 individual pixel points).
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Format the output into the requested list of lists
    all_black_shapes = []
    
    # for contour in contours:
    #     shape_points = []
    #     # Epsilon determines how much to simplify. 
    #     # A higher number means fewer points (blockier shapes).
    #     epsilon = 0.0005 * cv2.arcLength(contour, True)
    #     approx_contour = cv2.approxPolyDP(contour, epsilon, True)
        
    #     for point in approx_contour:
    #         x, y = point[0]
    #         shape_points.append((int(x), int(y)))
    #     # Extract the x, y coordinates from the OpenCV contour format

            
    #     # Optional: Only keep shapes that are actual polygons (3 or more points)
    #     # This helps filter out tiny 1-pixel noise dots in the image.
    #     if len(shape_points) >= 3:
    #         if cv2.contourArea(np.array(shape_points, dtype=np.int32)) > 200:
    #             all_black_shapes.append(shape_points)
    for contour in contours:
        shape_points = []
        
        # Extract the x, y coordinates from the OpenCV contour format
        for point in contour:
            x, y = point[0]
            shape_points.append((int(x), int(y)))
            
        # Optional: Only keep shapes that are actual polygons (3 or more points)
        # This helps filter out tiny 1-pixel noise dots in the image.
        if len(shape_points) >= 3:
            all_black_shapes.append(shape_points)
    print("List is complete")
    return all_black_shapes


# all_black_shapes = 
# image_file = "final_black_and_white_2.jpg" # Replace with your image name
    
    

# all_black_shapes = get_black_shapes_coordinates(image_file)
# tamaños = []
# for i in all_black_shapes:
#     tamaños.append(len(i))
# print(cv2.contourArea(np.array(all_black_shapes[4], dtype=np.int32)))
# --- Visualization ---
# pygame.init()
# width, height = 1300, 800
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Shape Visualization")

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # Draw background (white)
#     screen.fill((200, 200, 200))

#     # Draw black shapes
#     for shape in all_black_shapes:
#         if cv2.contourArea(np.array(shape, dtype=np.int32)) < 200:
#             continue
#         else:
#             # pygame.draw.polygon takes a list of (x, y) tuples
#             pygame.draw.polygon(screen, (0, 0, 0), shape)
#             # Draw outline to make them clearer
#             pygame.draw.polygon(screen, (50, 50, 50), shape, 2)

#     # Draw red dot
#     pygame.draw.circle(screen, (255, 0, 0), red_dot, 5)

#     pygame.display.flip()

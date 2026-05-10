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
    
    for contour in contours:
        shape_points = []
        # Epsilon determines how much to simplify. 
        # A higher number means fewer points (blockier shapes).
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx_contour = cv2.approxPolyDP(contour, epsilon, True)
        
        for point in approx_contour:
            x, y = point[0]
            shape_points.append((int(x), int(y)))
        # Extract the x, y coordinates from the OpenCV contour format

            
        # Optional: Only keep shapes that are actual polygons (3 or more points)
        # This helps filter out tiny 1-pixel noise dots in the image.
        if len(shape_points) >= 3:
            all_black_shapes.append(shape_points)

    return all_black_shapes

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    image_file = "final_black_and_white_2.jpg" # Replace with your image name
    
    shapes_list = get_black_shapes_coordinates(image_file)
    
    print(f"Total black shapes found: {len(shapes_list)}")
    
    # Print the coordinates of the first 3 shapes as an example
    for i in range(min(3, len(shapes_list))):
        print(f"Shape {i+1}: {shapes_list[i]}")
import cv2
import numpy as np

def extract_green_and_white(image_path, output_path):
    """
    Finds all Green and White pixels in an image, turns them pure White (#FFFFFF), 
    and turns all other colors Black (#000000).
    """
    # 1. Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load the image. Check the file path.")
        return

    # 2. Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 3. Define the HSV range for "Any type of Green"
    # Hue ~35 to 85 covers most greens. 
    # Saturation and Value are set above 40 to ignore grays/blacks.
    lower_green = np.array([35, 40, 40], dtype=np.uint8)
    upper_green = np.array([85, 255, 255], dtype=np.uint8)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # 4. Define the HSV range for "White"
    # White has any Hue (0-179), very low Saturation (0-40), and high Value/Brightness (200-255).
    lower_white = np.array([0, 0, 250], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)


    # grey_l = np.array([0, 0, 245], dtype=np.uint8)
    # grey_u = np.array([255, 255, 255], dtype=np.uint8)
    # white_mask = cv2.inRange(hsv_image, grey_l, grey_u)


    # 5. Combine the two masks
    # cv2.bitwise_or combines them. If a pixel is Green OR White, it becomes 255 (White).
    # All other pixels remain 0 (Black).
    combined_mask = cv2.bitwise_or(green_mask, white_mask)

    # 6. Save the output
    # The combined mask is already exactly what you want: a pure black and white image.
    cv2.imwrite(output_path, combined_mask)
    print(f"Success! Image saved to {output_path}")

# ==========================================
# Run the script
# ==========================================
if __name__ == "__main__":
    extract_green_and_white(
        image_path="map_mask.png", 
        output_path="final_black_and_white_2.jpg"
    )
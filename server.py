import os
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from shape import get_black_shapes_coordinates
from prue import extract_green_and_white
# Load environment variables
load_dotenv()
MAPBOX_API = os.getenv("MAPBOX_API")

app = Flask(__name__)


import cv2
import numpy as np

# def extract_green_and_white(image_path, output_path):
#     """
#     Finds all Green and White pixels in an image, turns them pure White (#FFFFFF), 
#     and turns all other colors Black (#000000).
#     """
#     # 1. Load the image
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Error: Could not load the image. Check the file path.")
#         return

#     # 2. Convert the image to HSV color space
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # 3. Define the HSV range for "Any type of Green"
#     # Hue ~35 to 85 covers most greens. 
#     # Saturation and Value are set above 40 to ignore grays/blacks.
#     lower_green = np.array([35, 40, 40], dtype=np.uint8)
#     upper_green = np.array([85, 255, 255], dtype=np.uint8)
#     green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

#     # 4. Define the HSV range for "White"
#     # White has any Hue (0-179), very low Saturation (0-40), and high Value/Brightness (200-255).
#     lower_white = np.array([0, 0, 235], dtype=np.uint8)
#     upper_white = np.array([255, 255, 255], dtype=np.uint8)
#     white_mask = cv2.inRange(hsv_image, lower_white, upper_white)


#     # grey_l = np.array([0, 0, 245], dtype=np.uint8)
#     # grey_u = np.array([255, 255, 255], dtype=np.uint8)
#     # white_mask = cv2.inRange(hsv_image, grey_l, grey_u)


#     # 5. Combine the two masks
#     # cv2.bitwise_or combines them. If a pixel is Green OR White, it becomes 255 (White).
#     # All other pixels remain 0 (Black).
#     combined_mask = cv2.bitwise_or(green_mask, white_mask)

#     # 6. Save the output
#     # The combined mask is already exactly what you want: a pure black and white image.
#     cv2.imwrite(output_path, combined_mask)


def get_blank():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    url = f"https://api.mapbox.com/styles/v1/mapbox/navigation-day-v1/static/{lng},{lat},16,0/1080x1080?access_token={MAPBOX_API}"

    

    try:
        response = requests.get(url)
        response.raise_for_status()

        filename = f"navigation.png"

        with open(filename, 'wb') as f:
            f.write(response.content)

        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')

    if not lat or not lng:
        return jsonify({"error": "Missing coordinates"}), 400
    
    get_blank()
    print(lat, lng)
    # Mapbox Static Image URL
    url = f'https://api.mapbox.com/styles/v1/mapbox/light-v11/static/{lng},{lat},16,0/1080x1080?access_token={MAPBOX_API}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Save image to directory
        filename = f"map_2.png"
        with open(filename, 'wb') as f:
            f.write(response.content)

        extract_green_and_white(image_path="map_2.png", output_path="final_black_and_white_2.jpg")
        black_shapes = get_black_shapes_coordinates(image_path="final_black_and_white_2.jpg")
    
        return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
        # print(e)

    # print(black_shapes)

@app.route('/')
def index():
    with open('index.html') as f:
        return render_template_string(f.read(), MAPBOX_API=MAPBOX_API)

if __name__ == '__main__':
    print("Server starting on http://localhost:5001")
    app.run(port=5001, debug=True)

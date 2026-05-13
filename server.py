import os
import requests
import cv2
import numpy as np
import json
import subprocess
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from prue import extract_green_and_white
from prueba2 import get_black_shapes_coordinates

load_dotenv()
MAPBOX_API = os.getenv("MAPBOX_API")

app = Flask(__name__)

def extract_shapes():
    extract_green_and_white(image_path="map_mask.png", output_path="final_black_and_white_2.jpg")
    print("Extracting shapes...")
    black_shapes = get_black_shapes_coordinates(image_path="final_black_and_white_2.jpg")
    return black_shapes

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    ball_count = data.get('ballCount', 1000)

    if not MAPBOX_API:
        return jsonify({"error": "MAPBOX_API key not found"}), 500

    # 1. Fetch Satellite Image for background
    sat_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{lng},{lat},15,0/1000x800?access_token={MAPBOX_API}"
    # 2. Fetch Street Image for shape extraction (Buildings are usually well-defined)
    mask_url = (
        f"https://api.mapbox.com/styles/v1/sergio321/cmp0epum7004001s70b56cut2/static/"
        f"{lng},{lat},15,0/1000x800"
        f"?access_token={MAPBOX_API}"
    )
    try:
        sat_res = requests.get(sat_url)
        mask_res = requests.get(mask_url)
        
        sat_res.raise_for_status()
        mask_res.raise_for_status()

        # Save satellite image
        bg_path = "map_bg.png"
        with open(bg_path, 'wb') as f:
            f.write(sat_res.content)

        mask_path = "map_mask.png"
        with open(mask_path, 'wb') as f:
            f.write(mask_res.content)

        # Extract shapes from mask
        shapes = extract_shapes()
        
        # Save config for ball.py
        config = {
            "bg_path": bg_path,
            "shapes": shapes,
            "center": [400, 300],
            "ball_count": int(ball_count)
        }
        with open('game_config.json', 'w') as f:
            json.dump(config, f)

        # Launch ball.py
        # Use a non-blocking call if you want the server to stay responsive, 
        # but here we just want to start the game.
        subprocess.Popen(["python3", "ball.py"])

        return jsonify({"status": "success", "message": "Game starting..."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def index():
    with open('index.html') as f:
        return render_template_string(f.read(), MAPBOX_API=MAPBOX_API)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

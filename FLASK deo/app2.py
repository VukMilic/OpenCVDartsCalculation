from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import os
from main_function import dart_points
from main_function import dart_points_clock

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    return jsonify({'message': 'Image uploaded successfully', 'file_path': filepath}), 200

@app.route('/get_hsv', methods=['POST'])
def get_hsv():
    data = request.json
    x = int(data.get('x'))
    y = int(data.get('y'))
    image_path = data.get('image_path')
    remove_image = int(data.get('remove_image'))

    print("Image path: {image_path}")

    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Ensure we don't go out of bounds
    if y < 0 or y >= hsv_image.shape[0] or x < 0 or x >= hsv_image.shape[1]:
        return jsonify({'error': 'Coordinates out of bounds'}), 400

    hsv_value = hsv_image[y, x].tolist()

    if remove_image == 1:
        # Delete the image file after processing
        try:
            os.remove(image_path)
        except OSError as e:
            return jsonify({'error': f"Error deleting file: {e}"}), 500
        
    return jsonify({'hsv_value': hsv_value}), 200

@app.route('/get_points_x01', methods=['POST'])
def get_points_x01():
    data = request.json
    image_path = data.get('image_path')
    tip_color_down = int(data.get('tip_color_down'))
    tip_color_up =  int(data.get('tip_color_up'))
    flight_color_down = int(data.get('flight_color_down'))
    flight_color_up =  int(data.get('flight_color_up'))

    points = dart_points(image_path, tip_color_down, tip_color_up, flight_color_down, flight_color_up)

    # Delete the image file after processing
    try:
        os.remove(image_path)
    except OSError as e:
        return jsonify({'error': f"Error deleting file: {e}"}), 500

    return jsonify({'points': points}), 200

@app.route('/get_points_clock', methods=['POST'])
def get_points_clock():
    data = request.json
    image_path = data.get('image_path')
    tip_color_down = int(data.get('tip_color_down'))
    tip_color_up =  int(data.get('tip_color_up'))
    flight_color_down = int(data.get('flight_color_down'))
    flight_color_up =  int(data.get('flight_color_up'))

    points = dart_points_clock(image_path, tip_color_down, tip_color_up, flight_color_down, flight_color_up)

    # Delete the image file after processing
    try:
        os.remove(image_path)
    except OSError as e:
        return jsonify({'error': f"Error deleting file: {e}"}), 500

    return jsonify({'points': points}), 200


if __name__ == '__main__':
    app.run(debug=True)


import os
import json
import cv2
from flask import Flask, Response, request, jsonify, render_template
from flask_cors import CORS
from urllib.parse import unquote

from app.fire_detection import detect_fire_combined
from app.fall_detection import detect_fall
from app.vehicle_crash import detect_crash
from app.video_handler import get_video_capture

app = Flask(__name__)
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_videos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_PASSWORD = "admin1234"
SETTINGS_FILE = "settings.json"

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/validate-admin', methods=['POST'])
def validate_admin():
    data = request.get_json()
    password = data.get("password")
    if password == ADMIN_PASSWORD:
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 401

@app.route('/admin-page')
def admin_page():
    return render_template('admin-page.html')

@app.route("/save-settings", methods=["POST"])
def save_settings():
    data = request.get_json()
    gmail = data.get("gmail", "").strip()
    if not gmail or "@" not in gmail:
        return jsonify(success=False, message="Invalid Gmail ID"), 400

    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"gmail": gmail}, f, indent=2)
    except Exception as e:
        return jsonify(success=False, message=f"Failed to save: {str(e)}"), 500

    return jsonify(success=True)

@app.route("/load-settings", methods=["GET"])
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return jsonify(success=False, message="No settings found"), 404

    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except Exception as e:
        return jsonify(success=False, message=f"Failed to load: {str(e)}"), 500

    return jsonify(success=True, gmail=settings.get("gmail"))

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify(success=False, message="No file part")
    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message="No selected file")

    filename = f"uploaded_{int(os.times()[4])}.mp4"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return jsonify(success=True, filename=filename)

@app.route('/video_feed/<source_type>/<path:source_path>')
@app.route('/video_feed/<source_type>', defaults={'source_path': None})
def video_feed(source_type, source_path):
    if source_path:
        source_path = unquote(source_path)  # decode percent encoding for URLs

    if source_type == "file":
        source_path = os.path.join(UPLOAD_FOLDER, source_path or "")
        if not os.path.isfile(source_path):
            return "File not found", 404

    cap = get_video_capture(source_type, source_path)
    if cap is None or not cap.isOpened():
        return "Error opening video stream", 404

    def generate_frames():
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Your detection pipeline
            frame, _ = detect_fire_combined(frame)

            fall_boxes = detect_fall(frame)
            for x1, y1, x2, y2 in fall_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Fall", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            crash_boxes = detect_crash(frame)
            for x1, y1, x2, y2 in crash_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, "Crash", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

from flask import Flask, Response
import cv2

from app.fire_detection import detect_fire
from app.fall_detection import detect_fall
from app.video_handler import get_video_capture

app = Flask(__name__)

@app.route('/video_feed/<source_type>/<path:source_path>')
@app.route('/video_feed/<source_type>', defaults={'source_path': None})
def video_feed(source_type, source_path):
    cap = get_video_capture(source_type, source_path)

    def generate_frames():
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # ---- Fire Detection ----
            fire_result = detect_fire(frame)
            for box in fire_result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
                cv2.putText(frame, f"🔥 Fire: {conf:.2f}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

            # ---- Fall Detection ----
            fall_boxes = detect_fall(frame)
            for x1, y1, x2, y2 in fall_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "🧍 Fall Detected", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Encode and stream frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, Response
import cv2

from app.fire_detection import detect_fire_combined
from app.fall_detection import detect_fall
from app.theft_detection import detect_theft
from app.video_handler import get_video_capture
# from app.alert import send_voicemail_alert  # Optional alert system

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

            # -------- Fire Detection (YOLO + CNN) --------
            frame, fire_detected = detect_fire_combined(frame)

            # -------- Fall Detection --------
            fall_boxes = detect_fall(frame)
            for x1, y1, x2, y2 in fall_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "🧍 Fall Detected", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # -------- Theft Detection --------
            theft_boxes = detect_theft(frame)
            for x1, y1, x2, y2 in theft_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.putText(frame, "🚨 Theft Detected", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

                # Optional: Trigger alert (voicemail/email)
                # send_voicemail_alert("🚨 Theft detected in surveillance feed.")

            # -------- Encode & Stream --------
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

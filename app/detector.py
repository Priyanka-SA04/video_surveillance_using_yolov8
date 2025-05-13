
from ultralytics import YOLO
import cv2
import uuid
from app.alert import send_alert

fall_model = YOLO("models/fall_model.pt")
fire_model = YOLO("models/fire_model.pt")
#accident_model = YOLO("models/accident_model.pt")
#suspicious_model = YOLO("models/suspicious_model.pt")

def detect_objects(frame):
    results = {
        "fall": fall_model(frame)[0],
        "fire": fire_model(frame)[0],
        #"accident": accident_model(frame)[0],
       # "suspicious": suspicious_model(frame)[0]
    }
    return results

def draw_detections(frame, results):
    for category, res in results.items():
        for box in res.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            label = f"{category}: {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def trigger_alerts(results, frame):
    for category, res in results.items():
        if len(res.boxes) > 0:
            filename = f"static/alerts/{uuid.uuid4().hex}.jpg"
            cv2.imwrite(filename, frame)
            send_alert(f"{category.title()} Detected", f"A {category} event was detected.", filename)

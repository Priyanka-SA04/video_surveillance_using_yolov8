# fire_detection.py
from app.alert import trigger_alert 
from ultralytics import YOLO
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load YOLOv8 fire detector (custom-trained)
yolo_model = YOLO('models/firedetection.pt')

# Load CNN classifier (MobileNetV2)
cnn_model = load_model('models/fire_classifier.h5')

def detect_fire_combined(frame):
    """
    Uses YOLOv8 to detect candidate fire regions and CNN to confirm.
    Returns: annotated frame, fire_detected_flag
    """
    fire_detected = False

    # Run YOLOv8 inference
    results = yolo_model.predict(source=frame, save=False, verbose=False)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = float(box.conf[0])

            # Extract region of interest (ROI)
            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                continue

            # Preprocess ROI for CNN
            resized_roi = cv2.resize(roi, (128, 128)).astype('float32') / 255.0
            cnn_input = np.expand_dims(resized_roi, axis=0)

            # Predict with CNN
            pred = cnn_model.predict(cnn_input, verbose=0)[0][0]

            if pred > 0.5:  # Confirmed fire
                fire_detected = True
                label = "FIRE"
                color = (0, 0, 255)
                trigger_alert(frame)

                # Annotate only if fire is confirmed
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame, fire_detected

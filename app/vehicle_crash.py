# app/vehicle_crash.py
from app.alert import trigger_alert 
from ultralytics import YOLO
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load YOLOv8 crash detection model
crash_model = YOLO("models/vehicle_crash.pt")

# Load CNN accident classifier model (MobileNetV2)
cnn_model = load_model("models/accident_detection.keras")

# Labels for CNN
CNN_CLASSES = ['accident', 'non-accident']

def detect_crash(frame):
    """
    Detects crash using YOLO and confirms using CNN classifier.
    Returns list of bounding boxes where both models agree.
    """
    results = crash_model.predict(source=frame, save=False, verbose=False)
    crash_boxes = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            if conf > 0.4:  # YOLO confidence threshold

                # Crop YOLO region
                crop = frame[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                # Preprocess for CNN
                resized = cv2.resize(crop, (224, 224))
                img_array = preprocess_input(resized.astype(np.float32))
                img_array = np.expand_dims(img_array, axis=0)

                # Predict with CNN
                preds = cnn_model.predict(img_array, verbose=0)
                class_idx = np.argmax(preds)
                class_label = CNN_CLASSES[class_idx]
                class_conf = preds[0][class_idx]

                if class_label == 'accident' and class_conf > 0.80:  # CNN threshold
                    crash_boxes.append((x1, y1, x2, y2))
                trigger_alert(frame)
    return crash_boxes

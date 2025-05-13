from ultralytics import YOLO
import numpy as np

# Load pretrained YOLOv8s model
fall_model = YOLO("models/yolov8s.pt")  # uses COCO classes

def is_fall(bbox, threshold=1.2):
    """
    Heuristic: If width > height or aspect ratio < threshold → possible fall
    """
    x1, y1, x2, y2 = bbox
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    aspect_ratio = height / (width + 1e-5)
    return aspect_ratio < threshold

def detect_fall(frame):
    """
    Uses YOLOv8s to detect people, then applies logic to identify falls.
    Returns a list of fall-like detections.
    """
    result = fall_model(frame)[0]
    fall_boxes = []

    for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
        class_id = int(cls.item())
        if class_id == 0:  # person
            x1, y1, x2, y2 = map(int, box.tolist())
            if is_fall([x1, y1, x2, y2]):
                fall_boxes.append([x1, y1, x2, y2])
    
    return fall_boxes

# from ultralytics import YOLO
# import numpy as np

# # Load pretrained YOLOv8s model
# fall_model = YOLO("models/yolov8s.pt")  # uses COCO classes

# def is_fall(bbox, threshold=1.2):
#     """
#     Heuristic: If width > height or aspect ratio < threshold → possible fall
#     """
#     x1, y1, x2, y2 = bbox
#     width = abs(x2 - x1)
#     height = abs(y2 - y1)
#     aspect_ratio = height / (width + 1e-5)
#     return aspect_ratio < threshold

# def detect_fall(frame):
#     """
#     Uses YOLOv8s to detect people, then applies logic to identify falls.
#     Returns a list of fall-like detections.
#     """
#     result = fall_model(frame)[0]
#     fall_boxes = []

#     for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
#         class_id = int(cls.item())
#         if class_id == 0:  # person
#             x1, y1, x2, y2 = map(int, box.tolist())
#             if is_fall([x1, y1, x2, y2]):
#                 fall_boxes.append([x1, y1, x2, y2])
    
#     return fall_boxes
from app.alert import trigger_alert  # Adjust the import path as needed

import cv2
import numpy as np
import tensorflow as tf
from ultralytics import YOLO
import mediapipe as mp
import math

# Load pretrained YOLOv8 model for person detection
yolo_model = YOLO("models/yolov8s.pt")

# Load the trained Keras MobileNetV2 fall detection model
cnn_model = tf.keras.models.load_model("models/fall_detection_model.keras")

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def extract_pose_features(frame, box):
    x1, y1, x2, y2 = box
    cropped = frame[y1:y2, x1:x2]
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    results = pose.process(cropped_rgb)
    return results.pose_landmarks

def torso_angle(pose_landmarks):
    # Get required landmarks indices for left shoulder, right shoulder, left hip, right hip
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24

    if not pose_landmarks:
        return None

    # Average left and right shoulders and hips for better robustness
    shoulders = [
        pose_landmarks.landmark[LEFT_SHOULDER],
        pose_landmarks.landmark[RIGHT_SHOULDER]
    ]
    hips = [
        pose_landmarks.landmark[LEFT_HIP],
        pose_landmarks.landmark[RIGHT_HIP]
    ]

    # Compute average x, y coordinates (normalized)
    shoulder_x = (shoulders[0].x + shoulders[1].x) / 2
    shoulder_y = (shoulders[0].y + shoulders[1].y) / 2
    hip_x = (hips[0].x + hips[1].x) / 2
    hip_y = (hips[0].y + hips[1].y) / 2

    # Vector from hip to shoulder
    dx = shoulder_x - hip_x
    dy = shoulder_y - hip_y

    # Calculate angle with respect to vertical axis (y-axis)
    # vertical vector points upward, so angle between vector and vertical axis is:
    angle_rad = math.atan2(dx, dy)  # dx first for atan2(y,x) to get angle from vertical
    angle_deg = abs(math.degrees(angle_rad))

    # Normalize angle between 0 and 90 degrees
    if angle_deg > 90:
        angle_deg = 180 - angle_deg

    return angle_deg

def preprocess_for_cnn(frame, box, target_size=(224, 224)):
    x1, y1, x2, y2 = box
    cropped = frame[y1:y2, x1:x2]
    resized = cv2.resize(cropped, target_size)
    normalized = resized / 255.0
    return np.expand_dims(normalized, axis=0)

def detect_fall(frame):
    results = yolo_model(frame)[0]
    fall_boxes = []

    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        class_id = int(cls.item())
        if class_id == 0:  # Person class in COCO
            x1, y1, x2, y2 = map(int, box.tolist())

            # Preprocess cropped person for CNN
            cnn_input = preprocess_for_cnn(frame, [x1, y1, x2, y2])
            prediction = cnn_model.predict(cnn_input, verbose=0)[0][0]

            # Get pose landmarks for this person
            pose_landmarks = extract_pose_features(frame, [x1, y1, x2, y2])
            angle = torso_angle(pose_landmarks)

            # Define threshold for angle (e.g., > 45 degrees means torso is tilted)
            FALL_ANGLE_THRESHOLD = 45

            # Decision logic: combine CNN and pose heuristic
            if prediction > 0.7 and angle is not None and angle > FALL_ANGLE_THRESHOLD:
                fall_boxes.append([x1, y1, x2, y2])
                trigger_alert(frame)
          
          

    return fall_boxes


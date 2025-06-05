from app.alert import trigger_alert 
from ultralytics import YOLO
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load YOLOv8 vehicle detection model (use yolov8s.pt or a custom trained vehicle model)
vehicle_model = YOLO("yolov8s.pt")

# Load CNN accident classifier (MobileNetV2)
cnn_model = load_model("models/accident_detection.keras")
CNN_CLASSES = ['accident', 'non-accident']

def detect_crash(frame):
    """
    Detect vehicles using YOLO, then use CNN to classify crash status.
    Returns list of bounding boxes where CNN confirms accident.
    """
    crash_boxes = []

    # Detect objects using YOLO
    results = vehicle_model.predict(source=[frame], save=False, verbose=False)
    result = results[0]

    for box in result.boxes:
        cls_id = int(box.cls[0])      # Class ID (e.g., car, truck)
        conf = float(box.conf[0])     # Confidence score

        # Only consider vehicle classes (COCO IDs: 2 = car, 3 = motorcycle, 5 = bus, 7 = truck)
        if cls_id in [2, 3, 5, 7] and conf > 0.5:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = frame[y1:y2, x1:x2]

            if crop.size == 0:
                continue

            # Preprocess for CNN
            resized = cv2.resize(crop, (224, 224))
            img_array = preprocess_input(resized.astype(np.float32))
            img_array = np.expand_dims(img_array, axis=0)

            # Predict accident status
            preds = cnn_model.predict(img_array, verbose=0)
            class_idx = np.argmax(preds)
            class_label = CNN_CLASSES[class_idx]
            class_conf = preds[0][class_idx]

            # Confirm accident with CNN
            if class_label == 'accident' and class_conf > 0.6:
                crash_boxes.append((x1, y1, x2, y2))
                trigger_alert(frame)

    return crash_boxes
# from app.alert import trigger_alert 
# from ultralytics import YOLO
# import cv2
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# # Load YOLOv8 vehicle detection model (use yolov8s.pt or a custom trained vehicle model)
# vehicle_model = YOLO("yolov8s.pt")

# # Load CNN accident classifier (MobileNetV2)
# cnn_model = load_model("models/accident_detection.keras")
# CNN_CLASSES = ['accident', 'non-accident']

# # Globals to keep track of previous frame for optical flow
# prev_gray = None

# # Threshold for optical flow magnitude to indicate crash movement
# OPTICAL_FLOW_THRESHOLD = 3.0

# def detect_crash(frame):
#     global prev_gray

#     crash_boxes = []

#     frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Calculate optical flow only if we have previous frame
#     flow = None
#     if prev_gray is not None:
#         flow = cv2.calcOpticalFlowFarneback(prev_gray, frame_gray,
#                                             None,
#                                             pyr_scale=0.5, levels=3, winsize=15,
#                                             iterations=3, poly_n=5, poly_sigma=1.2, flags=0)

#     # Detect objects using YOLO
#     results = vehicle_model.predict(source=[frame], save=False, verbose=False)
#     result = results[0]

#     for box in result.boxes:
#         cls_id = int(box.cls[0])      # Class ID (e.g., car, truck)
#         conf = float(box.conf[0])     # Confidence score

#         # Only consider vehicle classes (COCO IDs: 2 = car, 3 = motorcycle, 5 = bus, 7 = truck)
#         if cls_id in [2, 3, 5, 7] and conf > 0.5:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             crop = frame[y1:y2, x1:x2]

#             if crop.size == 0:
#                 continue

#             # Preprocess for CNN
#             resized = cv2.resize(crop, (224, 224))
#             img_array = preprocess_input(resized.astype(np.float32))
#             img_array = np.expand_dims(img_array, axis=0)

#             # Predict accident status
#             preds = cnn_model.predict(img_array, verbose=0)
#             class_idx = np.argmax(preds)
#             class_label = CNN_CLASSES[class_idx]
#             class_conf = preds[0][class_idx]

#             # Calculate optical flow magnitude inside vehicle box if flow exists
#             flow_magnitude_ok = False
#             if flow is not None:
#                 # Clip flow ROI inside frame bounds
#                 h, w = frame_gray.shape
#                 x1c, y1c = max(0, x1), max(0, y1)
#                 x2c, y2c = min(w, x2), min(h, y2)

#                 flow_roi = flow[y1c:y2c, x1c:x2c]
#                 if flow_roi.size > 0:
#                     mag, ang = cv2.cartToPolar(flow_roi[..., 0], flow_roi[..., 1])
#                     mean_magnitude = np.mean(mag)
#                     if mean_magnitude > OPTICAL_FLOW_THRESHOLD:
#                         flow_magnitude_ok = True

#             # Confirm accident only if CNN predicts accident AND optical flow indicates impact
#             if class_label == 'accident' and class_conf > 0.6 and flow_magnitude_ok:
#                 crash_boxes.append((x1, y1, x2, y2))
#                 trigger_alert(frame)

#     prev_gray = frame_gray.copy()

#     return crash_boxes





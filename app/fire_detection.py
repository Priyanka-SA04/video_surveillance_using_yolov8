from ultralytics import YOLO

# Load the trained fire detection model
fire_model = YOLO("models/firedetection.pt")

def detect_fire(frame):
    """
    Detect fire in the given frame using the fire YOLOv8 model.
    Returns: YOLO result object
    """
    return fire_model(frame)[0]

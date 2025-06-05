# import pytest
# import cv2
# import os
# import sys

# # Add project root to system path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app.fall_detection import detect_fall

# # Get base directory (project root)
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# def get_abs_path(relative_path):
#     """Converts relative path to absolute path based on project root"""
#     return os.path.join(BASE_DIR, relative_path)

# def load_image(relative_path):
#     """Loads image using absolute path"""
#     full_path = get_abs_path(relative_path)
#     if not os.path.exists(full_path):
#         raise FileNotFoundError(f"Image not found: {full_path}")
#     image = cv2.imread(full_path)
#     if image is None:
#         raise ValueError(f"Failed to read image: {full_path}")
#     return image

# # ✅ Pass test cases
# @pytest.mark.parametrize("image_path, expected_fall", [
#     ("tests/test_videos/fall1.jpg", True),
#     ("tests/test_videos/fall2.jpg", True),
#     ("tests/test_videos/nofall1.jpg", False),
#     ("tests/test_videos/nofall2.jpg", False),
#     ("tests/test_videos/nofall3.jpg", False),
# ])
# def test_detect_fall_pass_cases(request, image_path, expected_fall):
#     frame = load_image(image_path)
#     fall_boxes = detect_fall(frame)
#     detected_fall = len(fall_boxes) > 0
#     request.node._actual_fall = detected_fall 
#     assert detected_fall == expected_fall

# # ✅ Fail test cases (for expected failure)
# @pytest.mark.parametrize("image_path, expected_fall", [
#     ("tests/test_videos/fail1.jpg", True),
#     ("tests/test_videos/fail2.jpg", True),
# ])
# def test_detect_fall_fail_cases(request, image_path, expected_fall):
#     frame = load_image(image_path)
#     fall_boxes = detect_fall(frame)
#     detected_fall = len(fall_boxes) > 0
#     request.node._actual_fall = detected_fall
#     assert detected_fall == expected_fall, f"Fall not detected in {image_path} when expected"
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.fall_detection import detect_fall, torso_angle


# Dummy frame (simulate a 480p image)
dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# --- Mock Classes --- #
class MockYOLOBox:
    def __init__(self):
        self.xyxy = [np.array([100, 100, 200, 300])]
        self.cls = [np.array([0])]  # Person class

class MockYOLOResult:
    def __getitem__(self, index):
        return self

    @property
    def boxes(self):
        return MockYOLOBox()


# ---------- UNIT TESTS ---------- #

@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_detect_fall_one_person_fall_detected(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Should detect a fall when CNN predicts high and angle is high"""
    mock_yolo.return_value = [MockYOLOResult()]
    mock_cnn.predict.return_value = np.array([[0.9]])
    mock_pose.return_value = MagicMock()
    mock_angle.return_value = 60

    fall_boxes = detect_fall(dummy_frame)
    assert len(fall_boxes) == 1

@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_detect_fall_person_not_fallen_due_to_cnn(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Should NOT detect fall if CNN says no fall"""
    mock_yolo.return_value = [MockYOLOResult()]
    mock_cnn.predict.return_value = np.array([[0.1]])
    mock_pose.return_value = MagicMock()
    mock_angle.return_value = 60

    fall_boxes = detect_fall(dummy_frame)
    assert fall_boxes == []

@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_detect_fall_person_not_fallen_due_to_angle(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Should NOT detect fall if angle is below threshold"""
    mock_yolo.return_value = [MockYOLOResult()]
    mock_cnn.predict.return_value = np.array([[0.9]])
    mock_pose.return_value = MagicMock()
    mock_angle.return_value = 10

    fall_boxes = detect_fall(dummy_frame)
    assert fall_boxes == []

@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_detect_fall_pose_missing(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Should not crash if pose landmarks are missing"""
    mock_yolo.return_value = [MockYOLOResult()]
    mock_cnn.predict.return_value = np.array([[0.9]])
    mock_pose.return_value = None
    mock_angle.return_value = None

    fall_boxes = detect_fall(dummy_frame)
    assert fall_boxes == []

@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_detect_fall_multiple_people(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Should iterate over multiple person detections"""
    class MultiBox:
        def __init__(self):
            self.xyxy = [
                np.array([100, 100, 200, 300]),
                np.array([300, 100, 400, 300])
            ]
            self.cls = [np.array([0]), np.array([0])]

    class MultiResult:
        def __getitem__(self, index):
            return self

        @property
        def boxes(self):
            return MultiBox()

    mock_yolo.return_value = [MultiResult()]
    mock_cnn.predict.return_value = np.array([[0.9]])
    mock_pose.return_value = MagicMock()
    mock_angle.return_value = 60

    fall_boxes = detect_fall(dummy_frame)
    assert len(fall_boxes) == 2


# ---------- CONTROL FLOW TESTS ---------- #

def test_torso_angle_none():
    """Returns None if pose_landmarks is None"""
    assert torso_angle(None) is None

def test_torso_angle_low_angle():
    """Angle below threshold gives low degree"""
    pose_mock = MagicMock()
    lm = MagicMock()
    lm.x = 0.5
    lm.y = 0.5
    pose_mock.landmark = [None]*25
    pose_mock.landmark[11] = lm
    pose_mock.landmark[12] = lm
    pose_mock.landmark[23] = MagicMock(x=0.5, y=0.6)
    pose_mock.landmark[24] = MagicMock(x=0.5, y=0.6)
    angle = torso_angle(pose_mock)
    assert angle < 90

def test_torso_angle_high_angle():
    """Tests high torso tilt"""
    pose_mock = MagicMock()
    pose_mock.landmark = [None]*25
    pose_mock.landmark[11] = MagicMock(x=0.7, y=0.4)
    pose_mock.landmark[12] = MagicMock(x=0.6, y=0.4)
    pose_mock.landmark[23] = MagicMock(x=0.2, y=0.8)
    pose_mock.landmark[24] = MagicMock(x=0.1, y=0.8)
    angle = torso_angle(pose_mock)
    assert angle > 45


# ---------- DATA FLOW TEST ---------- #

@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_fall_data_flow_combined_decision(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Test if CNN and angle both must be satisfied"""
    mock_yolo.return_value = [MockYOLOResult()]
    mock_cnn.predict.return_value = np.array([[0.6]])  # barely above 0.5
    mock_pose.return_value = MagicMock()
    mock_angle.return_value = 47  # just above 45

    fall_boxes = detect_fall(dummy_frame)
    assert len(fall_boxes) == 1


# Optional: Edge case
@patch("app.fall_detection.yolo_model")
@patch("app.fall_detection.cnn_model")
@patch("app.fall_detection.extract_pose_features")
@patch("app.fall_detection.torso_angle")
def test_detect_fall_invalid_box(mock_angle, mock_pose, mock_cnn, mock_yolo):
    """Box coordinates outside image should not crash"""
    class EdgeBox:
        def __init__(self):
            self.xyxy = [np.array([600, 400, 800, 600])]
            self.cls = [np.array([0])]

    class EdgeResult:
        def __getitem__(self, index):
            return self
        @property
        def boxes(self):
            return EdgeBox()

    mock_yolo.return_value = [EdgeResult()]
    mock_cnn.predict.return_value = np.array([[0.9]])
    mock_pose.return_value = MagicMock()
    mock_angle.return_value = 60

    fall_boxes = detect_fall(dummy_frame)
    assert isinstance(fall_boxes, list)


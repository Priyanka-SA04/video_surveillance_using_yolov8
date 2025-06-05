import sys
import pytest
import numpy as np
import cv2

# Add your project root to sys.path so 'app' module is found
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.fire_detection import detect_fire_combined

# Mock classes to simulate YOLOv8 results and boxes

class MockBox:
    def __init__(self, xyxy, conf):
        # xyxy is a list or array-like with 4 coords: x1,y1,x2,y2
        self.xyxy = np.array([xyxy], dtype=float)
        self.conf = np.array([conf], dtype=float)

class MockResult:
    def __init__(self, boxes):
        # boxes should be a list of MockBox, but since the real code expects iterable boxes,
        # boxes here is a list and will be iterable
        self.boxes = boxes

class MockYOLOModel:
    def __init__(self, boxes_to_return):
        self.boxes_to_return = boxes_to_return

    def predict(self, source, save=False, verbose=False):
        # Always return a list with one MockResult containing the boxes
        return [MockResult(self.boxes_to_return)]

@pytest.fixture
def sample_frame():
    # Create a dummy frame (200x200, 3 channels, white)
    return np.ones((200, 200, 3), dtype=np.uint8) * 255

def test_detect_fire_confirmed(monkeypatch, sample_frame):
    # Patch YOLO model inside fire_detection to return one box with high confidence
    box = MockBox([50, 50, 100, 100], 0.9)
    monkeypatch.setattr('app.fire_detection.yolo_model', MockYOLOModel([box]))

    # Patch cnn_model.predict to always return >0.5 to confirm fire
    monkeypatch.setattr('app.fire_detection.cnn_model.predict', lambda x, verbose=0: np.array([[0.8]]))

    # Patch trigger_alert to track if called
    called = {}
    def fake_trigger_alert(frame):
        called['called'] = True
    monkeypatch.setattr('app.fire_detection.trigger_alert', fake_trigger_alert)

    annotated_frame, fire_flag = detect_fire_combined(sample_frame.copy())

    assert fire_flag is True
    assert 'called' in called
    # Check if rectangle (red) likely drawn (check pixel color near box coords)
    assert (annotated_frame[51, 51] == [0, 0, 255]).all()

def test_detect_fire_cnn_rejects(monkeypatch, sample_frame):
    # Box detected but CNN predicts below threshold (no fire)
    box = MockBox([30, 30, 80, 80], 0.8)
    monkeypatch.setattr('app.fire_detection.yolo_model', MockYOLOModel([box]))
    monkeypatch.setattr('app.fire_detection.cnn_model.predict', lambda x, verbose=0: np.array([[0.3]]))

    called = {}
    def fake_trigger_alert(frame):
        called['called'] = True
    monkeypatch.setattr('app.fire_detection.trigger_alert', fake_trigger_alert)

    annotated_frame, fire_flag = detect_fire_combined(sample_frame.copy())

    assert fire_flag is False
    assert 'called' not in called
    # No red rectangle drawn; pixel remains white
    assert (annotated_frame[31, 31] == [255, 255, 255]).all()

def test_detect_fire_no_boxes(monkeypatch, sample_frame):
    # YOLO returns no boxes detected
    monkeypatch.setattr('app.fire_detection.yolo_model', MockYOLOModel([]))
    monkeypatch.setattr('app.fire_detection.cnn_model.predict', lambda x, verbose=0: np.array([[1.0]]))

    called = {}
    def fake_trigger_alert(frame):
        called['called'] = True
    monkeypatch.setattr('app.fire_detection.trigger_alert', fake_trigger_alert)

    annotated_frame, fire_flag = detect_fire_combined(sample_frame.copy())

    assert fire_flag is False
    assert 'called' not in called

def test_detect_fire_multiple_boxes(monkeypatch, sample_frame):
    # Multiple boxes with mixed CNN predictions
    boxes = [
        MockBox([10, 10, 50, 50], 0.7),
        MockBox([60, 60, 120, 120], 0.9),
    ]
    monkeypatch.setattr('app.fire_detection.yolo_model', MockYOLOModel(boxes))

    # CNN predicts fire for first, no fire for second
    def cnn_predict(x, verbose=0):
        # x shape (1,128,128,3) so we can guess which box by size? We'll just alternate:
        # We'll always return >0.5 for first call, <0.5 for second call by using call count
        if not hasattr(cnn_predict, "call_count"):
            cnn_predict.call_count = 0
        cnn_predict.call_count += 1
        return np.array([[0.6 if cnn_predict.call_count == 1 else 0.3]])
    monkeypatch.setattr('app.fire_detection.cnn_model.predict', cnn_predict)

    called = {}
    def fake_trigger_alert(frame):
        called['called'] = True
    monkeypatch.setattr('app.fire_detection.trigger_alert', fake_trigger_alert)

    annotated_frame, fire_flag = detect_fire_combined(sample_frame.copy())

    assert fire_flag is True
    assert 'called' in called
    # At least one red rectangle should be drawn
    assert (annotated_frame[11, 11] == [0, 0, 255]).all()

def test_detect_fire_invalid_box(monkeypatch, sample_frame):
    # Box with invalid coordinates (empty roi)
    box = MockBox([10, 10, 5, 5], 0.95)  # x2 < x1, invalid box
    monkeypatch.setattr('app.fire_detection.yolo_model', MockYOLOModel([box]))
    monkeypatch.setattr('app.fire_detection.cnn_model.predict', lambda x, verbose=0: np.array([[1.0]]))

    called = {}
    def fake_trigger_alert(frame):
        called['called'] = True
    monkeypatch.setattr('app.fire_detection.trigger_alert', fake_trigger_alert)

    annotated_frame, fire_flag = detect_fire_combined(sample_frame.copy())

    # No fire should be detected since ROI is invalid
    assert fire_flag is False
    assert 'called' not in called

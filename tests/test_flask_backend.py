# import sys
# import os
# import pytest

# # Add root directory to Python path so it can find apps.py
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from apps import app  # <-- Now correctly imports your Flask app instance

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_homepage(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b"<html" in response.data.lower()

# def test_index_page(client):
#     response = client.get('/index')
#     assert response.status_code == 200
#     assert b"<html" in response.data.lower()

# def test_admin_validation_success(client):
#     response = client.post('/validate-admin', json={"password": "admin1234"})
#     assert response.status_code == 200
#     assert response.get_json()['success'] is True

# def test_admin_validation_fail(client):
#     response = client.post('/validate-admin', json={"password": "wrongpass"})
#     assert response.status_code == 401
#     assert response.get_json()['success'] is False


import sys
import os
import pytest
from io import BytesIO

# Add root directory so Python can find apps.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apps import app  # Flask app instance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data.lower()

def test_index(client):
    response = client.get('/index')
    assert response.status_code == 200
    assert b"<html" in response.data.lower()

def test_admin_page(client):
    response = client.get('/admin-page')
    assert response.status_code == 200
    assert b"<html" in response.data.lower()

def test_validate_admin_success(client):
    response = client.post('/validate-admin', json={"password": "admin1234"})
    assert response.status_code == 200
    assert response.get_json()['success'] is True

def test_validate_admin_fail(client):
    response = client.post('/validate-admin', json={"password": "wrong"})
    assert response.status_code == 401
    assert response.get_json()['success'] is False

def test_save_settings_success(client):
    response = client.post('/save-settings', json={"gmail": "test@example.com"})
    assert response.status_code == 200
    assert response.get_json()['success'] is True

def test_save_settings_invalid_email(client):
    response = client.post('/save-settings', json={"gmail": "invalid_email"})
    assert response.status_code == 400
    assert response.get_json()['success'] is False

def test_load_settings_success(client):
    client.post('/save-settings', json={"gmail": "test@example.com"})
    response = client.get('/load-settings')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert 'gmail' in json_data

def test_load_settings_not_found(client):
    if os.path.exists("settings.json"):
        os.remove("settings.json")
    response = client.get('/load-settings')
    assert response.status_code == 404
    assert response.get_json()['success'] is False

def test_upload_video_valid(client):
    dummy_video = BytesIO(b"fake video content")
    dummy_video.name = "dummy.mp4"
    response = client.post('/upload_video', content_type='multipart/form-data', data={
        'file': (dummy_video, dummy_video.name)
    })
    assert response.status_code == 200
    assert response.get_json()['success'] is True
    assert 'filename' in response.get_json()

def test_upload_video_no_file(client):
    response = client.post('/upload_video', content_type='multipart/form-data', data={})
    assert response.status_code == 200
    assert response.get_json()['success'] is False

def test_upload_video_empty_file(client):
    response = client.post('/upload_video', content_type='multipart/form-data', data={
        'file': (BytesIO(b''), '')
    })
    assert response.status_code == 200
    assert response.get_json()['success'] is False

def test_video_feed_file_not_found(client):
    response = client.get('/video_feed/file/nonexistent.mp4')
    assert response.status_code == 404

def test_video_feed_invalid_type(client):
    response = client.get('/video_feed/invalidsource')
    assert response.status_code == 404

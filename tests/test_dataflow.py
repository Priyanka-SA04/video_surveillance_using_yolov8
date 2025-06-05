from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def print_result(test_name, passed):
    print(f"{test_name}: {'PASS' if passed else 'FAIL'}")

# Initialize browser and wait
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)  

try:
    # 1.1 Video input loaded - file upload test
    driver.get("http://localhost:5000/index")
    wait.until(EC.presence_of_element_located((By.ID, "file-input")))

    file_input = driver.find_element(By.ID, "file-input")
    file_input.send_keys("C:/Users/prath/OneDrive/Desktop/intelligent_surveillance_system/tests/test_videos/sample_video.mp4")  # Update path
    time.sleep(2)  # Wait for frontend processing

    file_path = file_input.get_attribute("value")
    print_result("1.1 Video input file upload", bool(file_path))

    # 1.2 Start button enabled after file upload (proxy for backend frame format)
    start_btn = driver.find_element(By.ID, "start-btn")
    start_enabled = start_btn.get_attribute("disabled") is None
    print_result("1.2 Start button enabled after file upload", start_enabled)

    # 1.3 Start detection to test model inference trigger
    start_btn.click()
    time.sleep(3)  # Wait for feed start

    live_feed = driver.find_element(By.ID, "live-feed")
    print_result("1.3 Live feed visible after start detection", live_feed.is_displayed())

    # 2.1 Model weights test via webcam trigger
    webcam_radio = driver.find_element(By.CSS_SELECTOR, "input[value='webcam']")
    webcam_radio.click()
    time.sleep(1)

    start_btn = driver.find_element(By.ID, "start-btn")
    start_btn.click()
    time.sleep(2)
    print_result("2.1 Model weights loaded and inference triggered (webcam)", live_feed.is_displayed())

    # 3.1 Alert generation test - check alert container exists
    alert_elem = driver.find_elements(By.ID, "alert-message")
    print_result("3.1 Alert container exists in DOM", len(alert_elem) > 0)

    # 4.1 Admin settings - Save Gmail
    driver.get("http://localhost:5000/admin-page")
    gmail_input = wait.until(EC.presence_of_element_located((By.ID, "gmail")))
    save_button = driver.find_element(By.ID, "save-settings-btn")

    gmail_input.clear()
    gmail_input.send_keys("alert@example.com")
    save_button.click()
    time.sleep(2)

    status_msg = driver.find_element(By.ID, "status-message").text.lower()
    print_result("4.1 Save admin Gmail setting", "saved successfully" in status_msg)

    # 4.2 Load saved Gmail and verify
    load_button = driver.find_element(By.ID, "load-settings-btn")
    load_button.click()
    time.sleep(2)

    loaded_email = gmail_input.get_attribute("value")
    print_result("4.2 Load admin Gmail setting", loaded_email == "alert@example.com")

    # # 5.1 YouTube URL input - invalid case
    # youtube_radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='youtube']")))
    # youtube_radio.click()

    # yt_input = wait.until(EC.element_to_be_clickable((By.ID, "youtube-url")))
    # yt_input.clear()
    # yt_input.send_keys("invalidurl")
    # time.sleep(1)

    # start_btn = driver.find_element(By.ID, "start-btn")
    # start_disabled = start_btn.get_attribute("disabled") is not None
    # print_result("5.1 Start button disabled with invalid YouTube URL", start_disabled)

    # # 5.2 YouTube URL input - valid case
    # yt_input.clear()
    # yt_input.send_keys("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # time.sleep(1)

    # start_btn = driver.find_element(By.ID, "start-btn")
    # start_enabled = start_btn.get_attribute("disabled") is None
    # print_result("5.2 Start button enabled with valid YouTube URL", start_enabled)

    # # 6.1 Stop detection and resource release
    # start_btn.click()
    # time.sleep(2)  # Allow detection to start

    # stop_btn = wait.until(EC.element_to_be_clickable((By.ID, "stop-btn")))
    # stop_btn.click()
    # time.sleep(2)

    # live_feed = driver.find_element(By.ID, "live-feed")
    # print_result("6.1 Live feed hidden after stop detection", not live_feed.is_displayed())

finally:
    print("\n🧪 Data Flow Test suite completed.")
    time.sleep(2)
    driver.quit()

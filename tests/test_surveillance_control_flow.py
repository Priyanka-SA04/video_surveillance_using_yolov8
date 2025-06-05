from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Store results for HTML report
test_results = []

def print_result(test_name, passed, error_msg=""):
    status = "PASSED" if passed else "FAILED"
    test_results.append((test_name, status, error_msg))
    print(f"{test_name}: {'PASS' if passed else 'FAIL'}")

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # 1. HOME PAGE LOAD AND NAVIGATION TO INDEX PAGE
    driver.get("http://localhost:5000/")
    print_result("Home page load", "Intelligent Video Surveillance" in driver.title or "Intelligent Video Surveillance" in driver.page_source)

    try:
        btn_to_index = wait.until(EC.element_to_be_clickable((By.ID, "to-index")))
        btn_to_index.click()
        time.sleep(1)
        print_result("Navigate from Home to Index page", "Select Video Source" in driver.page_source)
    except Exception as e:
        print_result("Navigate from Home to Index page", False, str(e))

    # 2. INDEX PAGE - Video Source Selection and Controls
    driver.get("http://localhost:5000/index")
    wait.until(EC.presence_of_element_located((By.NAME, "video_source")))

    try:
        device_radio = driver.find_element(By.CSS_SELECTOR, "input[value='device']")
        device_radio.click()
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        print_result("Start button disabled with no file upload (device)", start_btn.get_attribute("disabled") is not None)
    except Exception as e:
        print_result("Start button disabled with no file upload (device)", False, str(e))

    try:
        file_input = driver.find_element(By.ID, "file-input")
        file_input.send_keys("C:/Users/prath/OneDrive/Desktop/intelligent_surveillance_system/tests/test_videos/sample_video.mp4")
        time.sleep(3)
        start_btn = driver.find_element(By.ID, "start-btn")
        start_enabled = start_btn.get_attribute("disabled") is None
        print_result("Start button enabled after valid file upload", start_enabled)
    except Exception as e:
        print_result("Start button enabled after valid file upload", False, str(e))

    try:
        webcam_radio = driver.find_element(By.CSS_SELECTOR, "input[value='webcam']")
        webcam_radio.click()
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        print_result("Start button enabled for webcam option", start_btn.get_attribute("disabled") is None)
    except Exception as e:
        print_result("Start button enabled for webcam option", False, str(e))

    try:
        youtube_radio = driver.find_element(By.CSS_SELECTOR, "input[value='youtube']")
        youtube_radio.click()
        yt_input = driver.find_element(By.ID, "youtube-url")
        yt_input.clear()
        yt_input.send_keys("invalidurl")
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        print_result("Start button disabled with invalid YouTube URL", start_btn.get_attribute("disabled") is not None)
    except Exception as e:
        print_result("Start button disabled with invalid YouTube URL", False, str(e))

    try:
        yt_input.clear()
        yt_input.send_keys("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        print_result("Start button enabled with valid YouTube URL", start_btn.get_attribute("disabled") is None)

        start_btn.click()
        time.sleep(2)
        live_feed = driver.find_element(By.ID, "live-feed")
        print_result("Live feed visible after start", live_feed.is_displayed())

        stop_btn = driver.find_element(By.ID, "stop-btn")
        stop_btn.click()
        time.sleep(1)
        print_result("Live feed hidden after stop", not live_feed.is_displayed())
    except Exception as e:
        print_result("Start/Stop Detection Flow", False, str(e))

    # 3. ADMIN PAGE - Login Tests
    driver.get("http://localhost:5000/admin-page")
    time.sleep(2)

    try:
        gmail_input = wait.until(EC.presence_of_element_located((By.ID, "gmail")))
        save_button = driver.find_element(By.ID, "save-settings-btn")

        gmail_input.clear()
        gmail_input.send_keys("invalidgmail")
        save_button.click()
        time.sleep(2)
        status_msg = driver.find_element(By.ID, "status-message").text
        print_result("Invalid Gmail submission (missing @)", "Invalid Gmail" in status_msg)
    except Exception as e:
        print_result("Invalid Gmail submission (missing @)", False, str(e))

    try:
        gmail_input.clear()
        save_button.click()
        time.sleep(2)
        status_msg = driver.find_element(By.ID, "status-message").text
        print_result("Empty Gmail submission", "Invalid Gmail" in status_msg)
    except Exception as e:
        print_result("Empty Gmail submission", False, str(e))

    try:
        gmail_input.clear()
        gmail_input.send_keys("alert@example.com")
        save_button.click()
        time.sleep(3)
        status_msg = driver.find_element(By.ID, "status-message").text
        print_result("Valid Gmail submission", "saved successfully" in status_msg.lower())
    except Exception as e:
        print_result("Valid Gmail submission", False, str(e))

    try:
        load_button = driver.find_element(By.ID, "load-settings-btn")
        load_button.click()
        time.sleep(2)
        loaded_value = gmail_input.get_attribute("value")
        print_result("Load saved Gmail value", loaded_value == "alert@example.com")
    except Exception as e:
        print_result("Load saved Gmail value", False, str(e))

finally:
    print("\n🧪 Test suite completed.")
    time.sleep(3)
    driver.quit()

# Generate HTML report
html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Selenium Test Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: white;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ccc;
                text-align: left;
            }}
            th {{
                background: #2c3e50;
                color: white;
            }}
            .PASSED {{
                background-color: #e8f8f5;
                color: #27ae60;
            }}
            .FAILED {{
                background-color: #fdecea;
                color: #e74c3c;
            }}
        </style>
    </head>
    <body>
        <h1>🧪 Intelligent Surveillance System Test Report</h1>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <table>
            <thead>
                <tr>
                    <th>Test Case</th>
                    <th>Status</th>
                    <th>Error</th>
                </tr>
            </thead>
            <tbody>
"""

# Add test results
for name, status, error in test_results:
    html += f"""
        <tr class="{status}">
            <td>{name}</td>
            <td>{'✔ Passed' if status == 'PASSED' else '✖ Failed'}</td>
            <td>{error if error else 'N/A'}</td>
        </tr>
    """

html += """
            </tbody>
        </table>
    </body>
    </html>
"""

# Save HTML
with open("selenium_test_report.html", "w", encoding="utf-8") as f:
    f.write(html)
    print("📄 HTML test report generated: selenium_test_report.html")

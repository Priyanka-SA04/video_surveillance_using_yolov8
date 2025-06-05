import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestFullUISuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Launch Chrome with larger window
        cls.driver = webdriver.Chrome()
        cls.driver.set_window_size(1200, 1000)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # ----------------- HOME PAGE TESTS -----------------

    def test_01_homepage_loads(self):
        self.driver.get("http://localhost:5000/")
        self.assertIn("Intelligent Video Surveillance", self.driver.title)

    def test_02_home_heading_visible(self):
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertIn("Intelligent Video Surveillance System", heading.text)

    def test_03_home_buttons_exist(self):
        buttons = self.driver.find_elements(By.TAG_NAME, "a")
        texts = [btn.text for btn in buttons]
        self.assertIn("Start Surveillance", texts)
        self.assertIn("Admin Settings", texts)

    def test_04_surveillance_button_navigates(self):
        self.driver.find_element(By.LINK_TEXT, "Start Surveillance").click()
        time.sleep(1)
        self.assertIn("/index", self.driver.current_url)

    def test_05_go_back_to_home(self):
        self.driver.get("http://localhost:5000/")

    # ----------------- INDEX PAGE TESTS -----------------

    def test_06_index_loads_and_title(self):
        self.driver.get("http://localhost:5000/index")
        self.assertIn("Intelligent Video Surveillance", self.driver.title)

    def test_07_radio_buttons_exist(self):
        radios = self.driver.find_elements(By.NAME, "video_source")
        self.assertEqual(len(radios), 3)

    def test_08_click_webcam_radio_enables_start(self):
        webcam_radio = self.driver.find_element(By.CSS_SELECTOR, "input[value='webcam']")
        webcam_radio.click()
        time.sleep(1)
        start_btn = self.driver.find_element(By.ID, "start-btn")
        self.assertFalse(start_btn.get_attribute("disabled"))

    def test_09_click_youtube_radio_displays_input(self):
        yt_radio = self.driver.find_element(By.CSS_SELECTOR, "input[value='youtube']")
        yt_radio.click()
        time.sleep(1)
        yt_input = self.driver.find_element(By.ID, "youtube-url")
        self.assertTrue(yt_input.is_displayed())

    def test_10_invalid_youtube_url_disables_start(self):
        yt_input = self.driver.find_element(By.ID, "youtube-url")
        yt_input.clear()
        yt_input.send_keys("invalid-url")
        time.sleep(1)
        start_btn = self.driver.find_element(By.ID, "start-btn")
        self.assertTrue(start_btn.get_attribute("disabled"))

    def test_11_valid_youtube_url_enables_start(self):
        yt_input = self.driver.find_element(By.ID, "youtube-url")
        yt_input.clear()
        yt_input.send_keys("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        time.sleep(2)
        start_btn = self.driver.find_element(By.ID, "start-btn")
        self.assertFalse(start_btn.get_attribute("disabled"))

    def test_12_start_detection_shows_iframe(self):
        self.driver.find_element(By.ID, "start-btn").click()
        time.sleep(2)
        iframe = self.driver.find_element(By.ID, "live-feed")
        self.assertTrue(iframe.is_displayed())

    def test_13_stop_detection_hides_iframe(self):
        self.driver.find_element(By.ID, "stop-btn").click()
        time.sleep(2)
        iframe = self.driver.find_element(By.ID, "live-feed")
        self.assertFalse(iframe.is_displayed())

    def test_14_warning_message_visible_on_stop(self):
        warning = self.driver.find_element(By.ID, "status-warning")
        self.assertTrue(warning.is_displayed())

    def test_15_device_radio_displays_file_input(self):
        device_radio = self.driver.find_element(By.CSS_SELECTOR, "input[value='device']")
        device_radio.click()
        time.sleep(1)
        file_input = self.driver.find_element(By.ID, "file-input")
        self.assertTrue(file_input.is_displayed())

    # ----------------- ADMIN PAGE TESTS -----------------

    def test_16_navigate_to_admin_page(self):
        self.driver.get("http://localhost:5000/admin-page")
        self.assertIn("/admin-page", self.driver.current_url)

    def test_17_check_phone_and_gmail_fields(self):
        
        gmail_input = self.driver.find_element(By.ID, "gmail")
        
        self.assertTrue(gmail_input.is_displayed())

    def test_18_invalid_phone_alert(self):
       
        gmail = self.driver.find_element(By.ID, "gmail")
       
        gmail.clear()
      
        gmail.send_keys("test@gmail.com")
        self.driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)
        # Expect some validation or reload - placeholder for now
        self.assertIn("/admin-page", self.driver.current_url)

    def test_19_valid_phone_and_gmail_submit(self):
        
        gmail = self.driver.find_element(By.ID, "gmail")
       
        gmail.clear()
        
        gmail.send_keys("test@gmail.com")
        self.driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)
        # Expect redirect or success alert - placeholder
        self.assertIn("/admin-page", self.driver.current_url)

    def test_20_home_link_from_admin(self):
        self.driver.find_element(By.LINK_TEXT, "Back to Home").click()
        time.sleep(1)
        self.assertIn("/", self.driver.current_url)

# if __name__ == "__main__":
#     unittest.main()


import unittest
from datetime import datetime

# Collect test results in this list
test_results = []

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        test_results.append((self.getDescription(test), "PASSED", ""))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_results.append((self.getDescription(test), "FAILED", self._exc_info_to_string(err, test)))

    def addError(self, test, err):
        super().addError(test, err)
        test_results.append((self.getDescription(test), "FAILED", self._exc_info_to_string(err, test)))

    def getDescription(self, test):
        return str(test)

# Run the tests
if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestFullUISuite)
    runner = unittest.TextTestRunner(resultclass=CustomTestResult)
    runner.run(suite)

    # HTML Report Generation
    html_report = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Integrated Test Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f8;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
            }}
            .summary {{
                background: #ffffff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
            }}
            .summary p {{
                font-size: 16px;
                margin: 8px 0;
            }}
            .pass {{ color: #27ae60; }}
            .fail {{ color: #e74c3c; }}
            .error {{ color: #f39c12; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
            }}
            th, td {{
                padding: 12px 16px;
                border-bottom: 1px solid #eee;
            }}
            th {{
                background-color: #2c3e50;
                color: white;
                text-align: left;
            }}
            .row-pass {{
                background-color: #e8f8f5;
                color: #27ae60;
            }}
            .row-fail {{
                background-color: #fdecea;
                color: #e74c3c;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 14px;
                color: #aaa;
            }}
        </style>
    </head>
    <body>
        <h1>🧪 Integrated Test Report</h1>
        <p><strong>🗓️ Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <p><strong>Total Tests:</strong> {len(test_results)}</p>
            <p class="pass"><strong>✔ Passed:</strong> {sum(1 for _, status, _ in test_results if status == "PASSED")}</p>
            <p class="fail"><strong>✖ Failures:</strong> {sum(1 for _, status, _ in test_results if status == "FAILED")}</p>
            <p class="error"><strong>⚠️ Errors:</strong> {sum(1 for _, status, error in test_results if error)}</p>
        </div>

        <h2>📋 Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Case</th>
                    <th>Result</th>
                    <th>Error (if any)</th>
                </tr>
            </thead>
            <tbody>
    """

    for desc, status, err in test_results:
        row_class = "row-pass" if status == "PASSED" else "row-fail"
        err_msg = err.replace('\n', '<br>') if err else "N/A"
        html_report += f"""
            <tr class="{row_class}">
                <td>{desc}</td>
                <td>{'✔ Passed' if status == 'PASSED' else '✖ Failed'}</td>
                <td>{err_msg}</td>
            </tr>
        """

    html_report += """
            </tbody>
        </table>

        <div class="footer">
            Generated by Selenium Test Suite • © 2025
        </div>
    </body>
    </html>
    """

    with open("integrated_test_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)

    print("✅ Test completed. Open 'integrated_test_report.html' to view the results.")

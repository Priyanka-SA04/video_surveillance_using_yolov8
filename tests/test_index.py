# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import os

# class VideoSurveillanceUITest(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.driver = webdriver.Chrome()
#         cls.driver.get("http://127.0.0.1:5000/index")  # Replace with your actual local path or server
#         cls.driver.maximize_window()

#     def test_01_select_youtube_source(self):
#         driver = self.driver
#         driver.find_element(By.CSS_SELECTOR, "input[value='youtube']").click()
#         yt_input = driver.find_element(By.ID, "youtube-url")
#         self.assertTrue(yt_input.is_displayed())

#     def test_02_valid_youtube_url_enables_start(self):
#         driver = self.driver
#         yt_input = driver.find_element(By.ID, "youtube-url")
#         yt_input.send_keys("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#         time.sleep(1)
#         start_btn = driver.find_element(By.ID, "start-btn")
#         self.assertFalse(start_btn.get_attribute("disabled"))

#     def test_03_invalid_youtube_url_disables_start(self):
#         driver = self.driver
#         yt_input = driver.find_element(By.ID, "youtube-url")
#         yt_input.clear()
#         yt_input.send_keys("invalid-link")
#         time.sleep(1)
#         start_btn = driver.find_element(By.ID, "start-btn")
#         self.assertTrue(start_btn.get_attribute("disabled"))

#     def test_04_select_webcam_source(self):
#         driver = self.driver
#         driver.find_element(By.CSS_SELECTOR, "input[value='webcam']").click()
#         time.sleep(1)
#         start_btn = driver.find_element(By.ID, "start-btn")
#         self.assertFalse(start_btn.get_attribute("disabled"))

#     def test_05_select_file_upload_shows_input(self):
#         driver = self.driver
#         driver.find_element(By.CSS_SELECTOR, "input[value='device']").click()
#         file_input = driver.find_element(By.ID, "file-input")
#         self.assertTrue(file_input.is_displayed())

#     def test_06_upload_file_enables_start(self):
#         driver = self.driver
#         file_input = driver.find_element(By.ID, "file-input")
#         test_video_path = os.path.abspath("tests/test_videos/sample_video.mp4")  # Ensure this file exists
#         file_input.send_keys(test_video_path)

#         # Wait for upload to complete and enable Start
#         WebDriverWait(driver, 5).until(
#             lambda d: not d.find_element(By.ID, "start-btn").get_attribute("disabled")
#         )
#         self.assertFalse(driver.find_element(By.ID, "start-btn").get_attribute("disabled"))

#     def test_07_start_button_shows_iframe(self):
#         driver = self.driver
#         driver.find_element(By.ID, "start-btn").click()
#         time.sleep(2)
#         iframe = driver.find_element(By.ID, "live-feed")
#         self.assertTrue(iframe.is_displayed())

#     def test_08_stop_button_hides_iframe(self):
#         driver = self.driver
#         driver.find_element(By.ID, "stop-btn").click()
#         time.sleep(1)
#         iframe = driver.find_element(By.ID, "live-feed")
#         self.assertFalse(iframe.is_displayed())

#     def test_09_status_warning_visible_on_stop(self):
#         driver = self.driver
#         status = driver.find_element(By.ID, "status-warning")
#         self.assertTrue(status.is_displayed())

#     def test_10_reselect_webcam_and_start(self):
#         driver = self.driver
#         driver.find_element(By.CSS_SELECTOR, "input[value='webcam']").click()
#         driver.find_element(By.ID, "start-btn").click()
#         time.sleep(2)
#         iframe = driver.find_element(By.ID, "live-feed")
#         self.assertTrue(iframe.is_displayed())

#     # ---------- ❌ FAIL CASES ----------

#     def test_fail_01_no_source_selected(self):
#         driver = self.driver
#         driver.refresh()
#         time.sleep(1)
#         start_btn = driver.find_element(By.ID, "start-btn")
#         self.assertTrue(start_btn.get_attribute("disabled"))

#     def test_fail_02_click_start_without_url_or_file(self):
#         driver = self.driver
#         driver.find_element(By.CSS_SELECTOR, "input[value='youtube']").click()
#         start_btn = driver.find_element(By.ID, "start-btn")
#         start_btn.click()
#         iframe = driver.find_element(By.ID, "live-feed")
#         self.assertFalse(iframe.is_displayed())  # Should not show because no valid URL

#     def test_fail_03_upload_wrong_file_type(self):
#         driver = self.driver
#         driver.find_element(By.CSS_SELECTOR, "input[value='device']").click()
#         file_input = driver.find_element(By.ID, "file-input")
#         fake_file = os.path.abspath("tests/test_videos/sample_test.txt")  # Ensure this dummy file exists
#         file_input.send_keys(fake_file)
#         time.sleep(2)
#         start_btn = driver.find_element(By.ID, "start-btn")
#         self.assertTrue(start_btn.get_attribute("disabled"))  # Start should remain disabled

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()

# if __name__ == "__main__":
#     unittest.main()

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime


class VideoSurveillanceUITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:5000/index")  # Change to your actual URL
        cls.driver.maximize_window()

    def test_01_select_youtube_source(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "input[value='youtube']").click()
        yt_input = driver.find_element(By.ID, "youtube-url")
        self.assertTrue(yt_input.is_displayed())

    def test_02_valid_youtube_url_enables_start(self):
        driver = self.driver
        yt_input = driver.find_element(By.ID, "youtube-url")
        yt_input.send_keys("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        self.assertFalse(start_btn.get_attribute("disabled"))

    def test_03_invalid_youtube_url_disables_start(self):
        driver = self.driver
        yt_input = driver.find_element(By.ID, "youtube-url")
        yt_input.clear()
        yt_input.send_keys("invalid-link")
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        self.assertTrue(start_btn.get_attribute("disabled"))

    def test_04_select_webcam_source(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "input[value='webcam']").click()
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        self.assertFalse(start_btn.get_attribute("disabled"))

    def test_05_select_file_upload_shows_input(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "input[value='device']").click()
        file_input = driver.find_element(By.ID, "file-input")
        self.assertTrue(file_input.is_displayed())

    def test_06_upload_file_enables_start(self):
        driver = self.driver
        file_input = driver.find_element(By.ID, "file-input")
        test_video_path = os.path.abspath("tests/test_videos/sample_video.mp4")
        file_input.send_keys(test_video_path)

        WebDriverWait(driver, 5).until(
            lambda d: not d.find_element(By.ID, "start-btn").get_attribute("disabled")
        )
        self.assertFalse(driver.find_element(By.ID, "start-btn").get_attribute("disabled"))

    def test_07_start_button_shows_iframe(self):
        driver = self.driver
        driver.find_element(By.ID, "start-btn").click()
        time.sleep(2)
        iframe = driver.find_element(By.ID, "live-feed")
        self.assertTrue(iframe.is_displayed())

    def test_08_stop_button_hides_iframe(self):
        driver = self.driver
        driver.find_element(By.ID, "stop-btn").click()
        time.sleep(1)
        iframe = driver.find_element(By.ID, "live-feed")
        self.assertFalse(iframe.is_displayed())

    def test_09_status_warning_visible_on_stop(self):
        driver = self.driver
        status = driver.find_element(By.ID, "status-warning")
        self.assertTrue(status.is_displayed())

    def test_10_reselect_webcam_and_start(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "input[value='webcam']").click()
        driver.find_element(By.ID, "start-btn").click()
        time.sleep(2)
        iframe = driver.find_element(By.ID, "live-feed")
        self.assertTrue(iframe.is_displayed())

    def test_fail_01_no_source_selected(self):
        driver = self.driver
        driver.refresh()
        time.sleep(1)
        start_btn = driver.find_element(By.ID, "start-btn")
        self.assertTrue(start_btn.get_attribute("disabled"))

    def test_fail_02_click_start_without_url_or_file(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "input[value='youtube']").click()
        start_btn = driver.find_element(By.ID, "start-btn")
        start_btn.click()
        iframe = driver.find_element(By.ID, "live-feed")
        self.assertFalse(iframe.is_displayed())

    def test_fail_03_upload_wrong_file_type(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "input[value='device']").click()
        file_input = driver.find_element(By.ID, "file-input")
        fake_file = os.path.abspath("tests/test_videos/sample_test.txt")
        file_input.send_keys(fake_file)
        time.sleep(2)
        start_btn = driver.find_element(By.ID, "start-btn")
        self.assertTrue(start_btn.get_attribute("disabled"))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


def generate_html_report(results):
    passed = [r[0] for r in results if r[1] == "PASS"]
    failed = [r[0] for r in results if r[1] == "FAIL"]
    total = len(results)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Video Surveillance UI Test Report</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white p-10">
        <h1 class="text-4xl font-bold mb-6 text-center text-teal-400">Video Surveillance UI Test Report</h1>
        <div class="max-w-4xl mx-auto">
            <table class="table-auto w-full border-collapse text-left text-white">
                <thead>
                    <tr class="bg-gray-800">
                        <th class="border px-4 py-2">Test Case</th>
                        <th class="border px-4 py-2">Result</th>
                    </tr>
                </thead>
                <tbody>
    """

    for test_name, status in results:
        row_class = "bg-green-800" if status == "PASS" else "bg-red-800"
        status_text = "PASSED" if status == "PASS" else "FAILED"
        html += f"""
            <tr class="{row_class}">
                <td class="border px-4 py-2">{test_name.replace('_', ' ').capitalize()}</td>
                <td class="border px-4 py-2 font-bold">{status_text}</td>
            </tr>
        """

    html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "ui_test_report.html")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n📝 HTML Report Generated: {report_path}")


if __name__ == "__main__":

    class ResultCollector(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.successes = []

        def addSuccess(self, test):
            super().addSuccess(test)
            self.successes.append(test)

    class CustomTestRunner(unittest.TextTestRunner):
        resultclass = ResultCollector

    suite = unittest.TestLoader().loadTestsFromTestCase(VideoSurveillanceUITest)
    runner = CustomTestRunner(verbosity=2)
    result = runner.run(suite)

    test_results = []
    for test in result.successes:
        test_results.append((test._testMethodName, "PASS"))
    for test, _ in result.failures + result.errors:
        test_results.append((test._testMethodName, "FAIL"))

    generate_html_report(test_results)

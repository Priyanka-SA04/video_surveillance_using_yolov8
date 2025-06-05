
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from io import StringIO
import sys
import datetime
import os

class SettingsPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()  # Replace with your WebDriver if needed
        cls.driver.implicitly_wait(15)
        cls.base_url = "http://127.0.0.1:5000/admin-page"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(self.base_url)

    def test_page_load(self):
        self.assertEqual(self.driver.title, "Settings Page")
        self.assertIsNotNone(self.driver.find_element(By.ID, "gmail"))
        self.assertIsNotNone(self.driver.find_element(By.ID, "save-settings-btn"))
        self.assertIsNotNone(self.driver.find_element(By.ID, "load-settings-btn"))
        self.assertIsNotNone(self.driver.find_element(By.ID, "status-message"))

    def test_save_valid_gmail(self):
        gmail_input = self.driver.find_element(By.ID, "gmail")
        gmail_input.clear()
        gmail_input.send_keys("valid@gmail.com")

        self.driver.find_element(By.ID, "save-settings-btn").click()
        status_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "status-message"))
        )
        self.assertIn("✅ Gmail ID saved successfully!", status_message.text)

    def test_save_invalid_gmail(self):
        gmail_input = self.driver.find_element(By.ID, "gmail")
        gmail_input.clear()
        gmail_input.send_keys("invalidgmail")

        self.driver.find_element(By.ID, "save-settings-btn").click()
        status_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "status-message"))
        )
        self.assertIn("❌ Invalid Gmail ID. Please try again.", status_message.text)

    def test_load_gmail(self):
        self.driver.find_element(By.ID, "load-settings-btn").click()

        gmail_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "gmail"))
        )
        self.assertTrue("@" in gmail_input.get_attribute("value"))

        status_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "status-message"))
        )
        self.assertIn("✅ Gmail ID loaded successfully!", status_message.text)

    def test_save_load_integration(self):
        gmail_input = self.driver.find_element(By.ID, "gmail")
        test_email = "integration@test.com"
        gmail_input.clear()
        gmail_input.send_keys(test_email)

        self.driver.find_element(By.ID, "save-settings-btn").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "status-message"))
        )

        self.driver.find_element(By.ID, "load-settings-btn").click()
        loaded_gmail = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "gmail"))
        )
        self.assertEqual(test_email, loaded_gmail.get_attribute("value"))

    def test_save_failed_mock(self):
        gmail_input = self.driver.find_element(By.ID, "gmail")
        gmail_input.clear()
        gmail_input.send_keys("fail@test.com")

        self.driver.find_element(By.ID, "save-settings-btn").click()
        status_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "status-message"))
        )
        self.assertIn("❌ Failed to save: Server error", status_message.text)

    def test_load_failed_mock(self):
        self.driver.find_element(By.ID, "load-settings-btn").click()
        status_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "status-message"))
        )
        self.assertIn("❌ Failed to load: Server error", status_message.text)


# --------- Dynamic HTML Reporting -----------

class HTMLTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)

    def get_report_data(self):
        return {
            'total': self.testsRun,
            'failures': self.failures,
            'errors': self.errors,
            'successes': self.successes,
        }

class HTMLTestRunner(unittest.TextTestRunner):
    def __init__(self, stream=sys.stdout, verbosity=1, title="Test Report", output="report.html"):
        super().__init__(stream, verbosity)
        self.output = output
        self.title = title

    def _makeResult(self):
        return HTMLTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        result = super().run(test)
        self.generate_html_report(result)
        return result

    def generate_html_report(self, result):
        report_data = result.get_report_data()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        passed = len(report_data['successes'])
        failed = len(report_data['failures']) + len(report_data['errors'])

        html = f"""
        <html>
        <head>
            <title>{self.title}</title>
            <style>
                body {{ font-family: Arial; }}
                .summary {{ margin-bottom: 20px; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                .error {{ color: orange; }}
            </style>
        </head>
        <body>
            <h1>{self.title}</h1>
            <p><strong>Date:</strong> {now}</p>
            <div class="summary">
                <p><strong>Total Tests:</strong> {report_data['total']}</p>
                <p class="pass"><strong>Passed:</strong> {passed}</p>
                <p class="fail"><strong>Failures:</strong> {len(report_data['failures'])}</p>
                <p class="error"><strong>Errors:</strong> {len(report_data['errors'])}</p>
            </div>
            <h2>Results:</h2>
            <ul>
        """

        for test in report_data['successes']:
            html += f"<li class='pass'>✔ {test}</li>"
        for test, msg in report_data['failures']:
            html += f"<li class='fail'>✖ {test}<br><pre>{msg}</pre></li>"
        for test, msg in report_data['errors']:
            html += f"<li class='error'>⚠ {test}<br><pre>{msg}</pre></li>"

        html += "</ul></body></html>"

        with open(self.output, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\n✅ HTML Test Report generated: {self.output}")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(SettingsPageTests)
    runner = HTMLTestRunner(verbosity=2, title="Settings Page Test Report", output="settings_test_report.html")
    runner.run(suite)

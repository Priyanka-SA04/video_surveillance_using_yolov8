from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up visible Chrome browser
driver = webdriver.Chrome()  # No headless mode; browser will be visible

# Define test results storage
test_results = []

def run_test(description, test_func):
    """Run a test case and record results."""
    try:
        test_func()
        test_results.append((description, "PASSED", ""))
    except Exception as e:
        test_results.append((description, "FAILED", str(e)))

# ---- Homepage Tests ----
def test_homepage_title():
    driver.get("http://127.0.0.1:5000/")  # Update with your homepage URL
    assert "Intelligent Video Surveillance System" in driver.title

def test_start_surveillance_button():
    driver.find_element(By.LINK_TEXT, "Start Surveillance")

def test_admin_button():
    driver.find_element(By.XPATH, "//button[contains(text(), 'Admin Page')]")

# ---- Page Transition Tests ----
def test_transition_to_admin_page():
    driver.find_element(By.XPATH, "//button[contains(text(), 'Admin Page')]").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "admin-modal")))
    driver.find_element(By.ID, "admin-password").send_keys("admin1234")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    WebDriverWait(driver, 5).until(lambda d: "Settings" in d.title)

# ---- Admin Page Tests ----
def test_admin_page_title():
    assert "Settings" in driver.title

def test_gmail_input_exists():
    driver.find_element(By.ID, "gmail")

def test_save_button_exists():
    driver.find_element(By.ID, "save-settings-btn")

def test_load_button_exists():
    driver.find_element(By.ID, "load-settings-btn")

def test_invalid_gmail_error():
    gmail_input = driver.find_element(By.ID, "gmail")
    gmail_input.clear()
    gmail_input.send_keys("invalid-email")
    driver.find_element(By.ID, "save-settings-btn").click()
    error_message = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.ID, "status-message"))
    ).text
    assert "Invalid Gmail ID" in error_message

def test_valid_gmail_success():
    gmail_input = driver.find_element(By.ID, "gmail")
    gmail_input.clear()
    gmail_input.send_keys("test@gmail.com")
    driver.find_element(By.ID, "save-settings-btn").click()
    success_message = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.ID, "status-message"))
    ).text
    assert "Gmail ID saved successfully" in success_message

def test_load_gmail():
    driver.find_element(By.ID, "load-settings-btn").click()
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.ID, "status-message"))
    )
    gmail_value = driver.find_element(By.ID, "gmail").get_attribute("value")
    assert gmail_value == "test@gmail.com"  # Replace with your test value

# ---- Run Tests ----
driver.get("http://127.0.0.1:5000/")  # Start from homepage

# Homepage tests
run_test("Homepage title is displayed", test_homepage_title)
run_test("Start Surveillance button exists", test_start_surveillance_button)
run_test("Admin Page button exists", test_admin_button)

# Page transition test
run_test("Transition from homepage to admin page", test_transition_to_admin_page)

# Admin page tests
run_test("Admin page title is displayed", test_admin_page_title)
run_test("Gmail input field exists", test_gmail_input_exists)
run_test("Save Settings button exists", test_save_button_exists)
run_test("Load Saved Gmail button exists", test_load_button_exists)
run_test("Invalid Gmail shows error message", test_invalid_gmail_error)
run_test("Valid Gmail shows success message", test_valid_gmail_success)
run_test("Load Saved Gmail retrieves Gmail", test_load_gmail)

driver.quit()

# ---- Generate Tailwind-styled HTML Report ----
# html_report = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Integrated Test Report</title>
#     <script src="https://cdn.tailwindcss.com"></script>
# </head>
# <body class="bg-gray-900 text-white p-10">
#     <h1 class="text-4xl font-bold mb-6 text-center text-teal-400">Integrated Test Report</h1>
#     <div class="max-w-4xl mx-auto">
#         <table class="table-auto w-full border-collapse text-left text-white">
#             <thead>
#                 <tr class="bg-gray-800">
#                     <th class="border px-4 py-2">Test Case</th>
#                     <th class="border px-4 py-2">Result</th>
#                     <th class="border px-4 py-2">Error (if any)</th>
#                 </tr>
#             </thead>
#             <tbody>
# """

# for desc, status, err in test_results:
#     row_color = "bg-green-800" if status == "PASSED" else "bg-red-800"
#     html_report += f"""
#         <tr class="{row_color}">
#             <td class="border px-4 py-2">{desc}</td>
#             <td class="border px-4 py-2 font-bold">{status}</td>
#             <td class="border px-4 py-2">{err}</td>
#         </tr>
#     """

# html_report += """
#             </tbody>
#         </table>
#     </div>
# </body>
# </html>
# """

# # Save to file
# with open("integrated_test_report.html", "w") as f:
#     f.write(html_report)

# print("✅ Test completed. Open 'integrated_test_report.html' to view the results.")
# ---- Updated Generate Tailwind-styled HTML Report ----
html_report = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Integrated Test Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f8;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
        }
        .summary {
            background: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
        }
        .summary p {
            font-size: 16px;
            margin: 8px 0;
        }
        .pass { color: #27ae60; }
        .fail { color: #e74c3c; }
        .error { color: #f39c12; }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
        }
        th, td {
            padding: 12px 16px;
            border-bottom: 1px solid #eee;
        }
        th {
            background-color: #2c3e50;
            color: white;
            text-align: left;
        }
        .row-pass {
            background-color: #e8f8f5;
            color: #27ae60;
        }
        .row-fail {
            background-color: #fdecea;
            color: #e74c3c;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 14px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <h1>🧪 Integrated Test Report</h1>
    <p><strong>🗓️ Date:</strong> 2025-05-24 12:20:00</p>

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
    html_report += f"""
        <tr class="{row_class}">
            <td>{desc}</td>
            <td>{'✔ Passed' if status == 'PASSED' else '✖ Failed'}</td>
            <td>{err if err else 'N/A'}</td>
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

# Save to file
with open("integrated_test_report.html", "w") as f:
    f.write(html_report)

print("✅ Test completed. Open 'integrated_test_report.html' to view the results.")

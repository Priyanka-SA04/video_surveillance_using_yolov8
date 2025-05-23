import os
import time
import json
import yagmail
from playsound import playsound
import cv2

# Path to the settings.json
SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")

# Global variables to track alert state
last_alert_time = 60
alert_triggered = False
ALERT_DURATION = 10  # seconds

def load_gmail():
    """Load recipient email from settings.json."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            return settings.get("gmail")
    return None

def send_email_alert(image_path):
    """Send an alert email with a frame attachment."""
    recipient = load_gmail()
    if not recipient:
        print("❌ Gmail not configured in settings.json")
        return

    try:
        # Sender credentials
        sender_email = "prathikshanayak.04@gmail.com"
        app_password = "qymx fqhb ljxw iuqx"  # Replace with Gmail app password

        yag = yagmail.SMTP(sender_email, app_password)

        subject = "🚨 ALERT: Suspicious Activity Detected"
        body = "A suspicious activity was detected. See the attached frame for details."

        # Send with attachment
        yag.send(to=recipient, subject=subject, contents=body, attachments=image_path)
        print("✅ Alert email sent with frame attached.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def play_alert_sound():
    """Play alert sound."""
    try:
        sound_path = os.path.join(os.getcwd(), "app", "alert_sound.mp3")
        playsound(sound_path)
    except Exception as e:
        print(f"❌ Could not play alert sound: {e}")

def trigger_alert(frame):
    """Trigger alert after detection persists for 5 seconds with frame snapshot."""
    global last_alert_time, alert_triggered

    current_time = time.time()
    if not alert_triggered:
        last_alert_time = current_time
        alert_triggered = True
    elif current_time - last_alert_time >= ALERT_DURATION:
        # Save current frame
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join("app", f"detected_frame_{timestamp}.jpg")
        cv2.imwrite(screenshot_path, frame)

        # Play sound and send email with image
        play_alert_sound()
        send_email_alert(screenshot_path)

        # Reset
        alert_triggered = False
        last_alert_time = 15
    else:
        print(f"⏳ Alert waiting: {int(current_time - last_alert_time)}s")

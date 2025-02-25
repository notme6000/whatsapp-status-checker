import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pushbullet import Pushbullet
import signal
import sys

# Initialize push notifications
PUSHBULLET_API_KEY = "pushbullent api key"  # Add your Pushbullet API key here
pb = Pushbullet(PUSHBULLET_API_KEY)

def send_notification(message):
    """Send a push notification via Pushbullet."""
    pb.push_note("WhatsApp Monitor", message)

def monitor_contact(driver, target_name):
    """Monitor the contact's online status."""
    try:
        while True:
            try:
                # Locate the "online" status element in the DOM
                status = driver.find_element(By.XPATH, "//span[@title='online']")
                send_notification(f"{target_name} is online!")
                print(f"{target_name} is online!")
                time.sleep(60)  # Wait for 1 minute before rechecking
            except Exception:
                print(f"{target_name} is offline.")
                send_notification(f"{target_name} is offline.")
                time.sleep(10)  # Check again after 10 seconds
    except KeyboardInterrupt:
        print("Monitoring stopped.")

def cleanup_and_exit(driver):
    """Clean up resources and exit."""
    print("Exiting and cleaning up...")
    driver.quit()
    sys.exit(0)

def main():
    # Path to chromedriver and Chrome binary
    chromedriver_path = "/home/notme6000/my-projects/alan-alert/chromedriver-linux64/chromedriver"
    chrome_binary_path = "/home/notme6000/my-projects/alan-alert/chrome-linux64/chrome"

    # Directory to store persistent Chrome user data
    user_data_dir = "/home/notme6000/my-projects/alan-alert/chrome-user-data"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Use persistent user data directory
    chrome_options.binary_location = chrome_binary_path  # Set custom Chrome binary path
    chrome_options.add_argument("--start-maximized")  # Start Chrome maximized

    # Initialize ChromeDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Handle cleanup on exit
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup_and_exit(driver))
    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup_and_exit(driver))

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")
    print("Please scan the QR code to log in to WhatsApp Web (only needed once).")

    # Wait for user to scan the QR code
    input("Press Enter after logging in and opening the target chat...")

    # Ask for the contact's name
    target_name = input("Enter the name of the contact to monitor: ")

    # Search and open the target chat
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
    search_box.send_keys(target_name)
    time.sleep(2)
    driver.find_element(By.XPATH, f"//span[@title='{target_name}']").click()

    # Start monitoring the contact
    monitor_contact(driver, target_name)

if __name__ == "__main__":
    main()

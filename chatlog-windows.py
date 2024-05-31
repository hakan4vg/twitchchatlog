"""
Created on Fri May 31 23:26:10 2024

@author: reul
"""

import os
import time
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Paths to the ChromeDriver and Chrome browser executable
CHROME_DRIVER_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "chromedriver.exe")
CHROME_EXECUTABLE_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

# Check if ChromeDriver is installed
def check_and_install_chromedriver():
    if not os.path.exists(CHROME_DRIVER_PATH):
        print("ChromeDriver is not installed. Installing...")
        url = "https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_win32.zip"  # Update this URL to the latest version if needed
        response = requests.get(url)
        with open(os.path.join(os.path.expanduser("~"), "Downloads", "chromedriver.zip"), "wb") as file:
            file.write(response.content)
        with zipfile.ZipFile(os.path.join(os.path.expanduser("~"), "Downloads", "chromedriver.zip"), "r") as zip_ref:
            zip_ref.extractall(os.path.join(os.path.expanduser("~"), "Downloads"))
        os.remove(os.path.join(os.path.expanduser("~"), "Downloads", "chromedriver.zip"))
        print("ChromeDriver installed successfully.")
    else:
        print("ChromeDriver is already installed.")

check_and_install_chromedriver()

# Get the current user's username
username = os.getlogin()

options = Options()
options.binary_location = CHROME_EXECUTABLE_PATH
service = Service(CHROME_DRIVER_PATH)
options.add_argument(f"user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Default")
driver = webdriver.Chrome(service=service, options=options)

def fetch_chat_messages(stream_name, username):
    url = f"https://www.twitch.tv/popout/{stream_name}/viewercard/{username}"
    driver.get(url)
    time.sleep(2)  # Allow time for page to load

    messages = []
    container_element = driver.find_element(By.CLASS_NAME, "simplebar-scroll-content")  # Change this class if needed

    # Get initial div height
    last_height = driver.execute_script("return arguments[0].scrollHeight", container_element)

    # Scroll to the top to load all chat history
    while True:
        # Scroll to the top
        driver.execute_script("arguments[0].scrollTo(0, 0)", container_element)
        time.sleep(0.5)  # Wait for new messages to load
        
        # Get the new div height after scrolling
        new_height = driver.execute_script("return arguments[0].scrollHeight", container_element)
        
        # Check if new messages loaded by comparing heights
        if new_height == last_height:
            break  # No new messages loaded, break out of loop
        
        # Update last height
        last_height = new_height

    # Get all existing messages after all messages are loaded
    elements = driver.find_elements(By.CLASS_NAME, "vcml-message")
    for element in elements:
        timestamp = element.find_element(By.CLASS_NAME, "vcml-message__timestamp").text
        author = element.find_element(By.CLASS_NAME, "message-author__display-name").text
        message = element.find_element(By.CLASS_NAME, "text-fragment").text
        messages.append(f"{timestamp} {author}: {message}")

    return messages

if __name__ == "__main__":
    stream_name = input("Enter the stream name: ")

    while True:
        username = input("Enter the username: (CTRL+Z to exit)")
        if username:
            print("Please wait while gathering messages")
        if not username:
            break

        messages = fetch_chat_messages(stream_name, username)
        
        # Output messages
        #for message in messages:
        #   print(message)

        # Save messages to a file
        with open(f"{username}_messages.txt", "w") as file:
            for message in messages:
                file.write(message + "\n")

    driver.quit()

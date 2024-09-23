from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Selenium WebDriver (using Chrome)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)
# Delinea Secret Server URL and credentials
login_url = os.getenv("LOGIN_SITE")
secrets_url = os.getenv("API_SITE")
username = os.getenv("EMAIL")
password = os.getenv("PASSWD")
secret_id = "4143"


# Function to log in to Secret Server
def login_to_secret_server():
    driver.get(login_url)

    # Wait for the login page to load
    time.sleep(3)

    # Find and fill in the username and password fields
    username_field = driver.find_element(By.ID, "UserNameTextBox")
    password_field = driver.find_element(By.ID, "PasswordTextBox")

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    login_button = driver.find_element(By.ID, "LoginButton")
    login_button.click()

    # Wait for the page to load
    time.sleep(3)


# Function to navigate to the secret and perform checkout
def checkout_secret(secret_id):
    # Navigate to the secret with the given ID
    driver.get(f"{secrets_url}/app/#/secrets/checkout/{secret_id}")

    # Wait for the secret page to load
    time.sleep(3)

    try:
        # Click on the "Check Out" button
        checkout_button = driver.find_element(By.ID, "checkout-button")
        checkout_button.click()

        # Wait for the action to complete
        time.sleep(3)
        print(f"Secret {secret_id} checked out successfully.")

    except Exception as e:
        print(f"Failed to checkout secret {secret_id}: {str(e)}")

    # Wait for the page to load
    time.sleep(3)


# Function to check-in the secret
def checkin_secret(secret_id):
    try:
        # Click on the "Check In Options" button
        checkin_option_button = driver.find_element(
            By.ID,
            "checkout-approval-options-menu-button",
        )
        checkin_option_button.click()

        time.sleep(3)
        # Click on the "Check In" button
        checkin_button = driver.find_element(
            By.ID,
            "option-menu-check-in",
        )
        checkin_button.click()
        # Wait for the action to complete
        time.sleep(3)
        print(f"Secret {secret_id} checked in successfully.")

    except Exception as e:
        print(f"Failed to checkin secret {secret_id}: {str(e)}")


# Main automation sequence
try:
    # Log in to Secret Server
    login_to_secret_server()

    # Checkout the secret
    checkout_secret(secret_id)

    # Checkin the secret
    checkin_secret(secret_id)

finally:
    # Close the browser window
    driver.quit()

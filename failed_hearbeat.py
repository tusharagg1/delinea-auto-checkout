import time
import sys
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def GetFailedHeartbeatSecrets():
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }
    resp = requests.get(api + "/secrets/?take=99999", headers=headers)
    if resp.status_code not in (200, 304):
        raise Exception(
            "Error retrieving Secrets. %s %s" % (resp.status_code, resp)
        )
    secrets = resp.json()
    df = pd.DataFrame(secrets["records"])
    # Filter rows where 'lastHeartBeatStatus' is 'Failed'
    status_filters = [
        "Failed",
        "UnableToConnect",
        "AccountLockedOut",
        "UnknownError",
    ]
    secret_templates = [
        "ATCO Active Directory",
        "ATCO Active directory account",
        "ATCO Active directory account -NO Heartbeat",
        "ATCO Active directory account RDP/PUTTY",
        "ATCO Active directory account-linux",
        "ATCO Active directory account-linux-Ansible-Heartbeat",
        "ATCO RSA POC Domain Controllers Active Directory Account",
        "ATCO EXT AD Secret Template",
    ]
    secret_templates_windows=[
        "Windows Account - 60",
    ]
    failed_heartbeats = df[
        df["secretTemplateName"].isin(secret_templates)
        & df["lastHeartBeatStatus"].isin(status_filters)
    ].id.tolist()  # Convert to a list
    
    failed_heartbeats_win = df[
        df["secretTemplateName"].isin(secret_templates_windows)
        & df["lastHeartBeatStatus"].isin(status_filters)
    ].id.tolist()  # Convert to a list
    
    return failed_heartbeats

# Set up Selenium WebDriver (using Chrome)
chrome_driver_path = ''
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Delinea Secret Server URL and credentials
login_url = ""
secrets_url = ""
username = ""
password = ""
authApi = "/oauth2/token"
api = secrets_url + "/api/v2"
token = ""
def login_to_secret_server():
    driver.get(login_url)
    time.sleep(5)
    username_field = driver.find_element(By.ID, "input28")
    password_field = driver.find_element(By.ID, "input36")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button = driver.find_element(By.CLASS_NAME, "button-primary")
    login_button.click()
    time.sleep(3)
    push_button = driver.find_element(By.CLASS_NAME, "link-button")
    push_button.click()
    time.sleep(15)
    push_button = driver.find_element(By.CLASS_NAME, "chiclet--action")
    push_button.click()
    href_value = ""
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//a[@href="{href_value}"]'))
    )
    element.click()
    time.sleep(10)

# Function to checkout the secret
def checkout_secret(secret_id):
    driver.get(f"{secrets_url}/app/#/secrets/checkout/{secret_id}")
    time.sleep(10)
    try:
        checkout_button = driver.find_element(By.XPATH, "//*[@id='checkout-button' or @id='force-check-in']")
        checkout_button.click()
        print(f"Secret {secret_id} checked out successfully.")
        time.sleep(10)
        #test case senario__________________________________________________________________________________________________________Start
        if driver.find_element(By.XPATH, "//*[@id='checkout-button']"):
            checkout_button = driver.find_element(By.XPATH, "//*[@id='checkout-button']")
            checkout_button.click()
            print(f"Secret {secret_id} checked out successfully.")
        elif(driver.find_element(By.ID, "checkout-approval-options-menu-button")):
            try:
                checkin_option_button = driver.find_element(By.ID, "checkout-approval-options-menu-button")
                checkin_option_button.click()
                time.sleep(10)
                checkin_button = driver.find_element(By.ID, "option-menu-check-in")
                checkin_button.click()
                time.sleep(5)
                print(f"Secret {secret_id} checked in successfully.")
            except Exception as e:
                print(f"Failed to checkin secret {secret_id}: {str(e)}")
                time.sleep(5)
            #test case senario__________________________________________________________________________________________________________End--Delete in case of Disaster
        print(f"Secret {secret_id} checked out successfully.")
    except Exception as e:
       print(f"Failed to checkout secret {secret_id}: {str(e)}")   
    time.sleep(15)  

# Function to check-in the secret
def checkin_secret(secret_id):
    try:
        checkin_option_button = driver.find_element(By.ID, "checkout-approval-options-menu-button")
        checkin_option_button.click()
        time.sleep(10)
        checkin_button = driver.find_element(By.ID, "option-menu-check-in")
        checkin_button.click()
        time.sleep(5)
        print(f"Secret {secret_id} checked in successfully.")
    except Exception as e:
        print(f"Failed to checkin secret {secret_id}: {str(e)}")

# Main automation sequence
try:
    # Log in to Secret Server
    login_to_secret_server()
    
    # Get the list of failed heartbeat secrets
    failed_heartbeats_before = GetFailedHeartbeatSecrets()
    print(len(failed_heartbeats_before))
    print(failed_heartbeats_before)
    
    # Iterate over each secret ID and perform checkout and check-in
    for secret_id in failed_heartbeats_before:
        checkout_secret(secret_id)
        checkin_secret(secret_id)
    failed_heartbeats_after = GetFailedHeartbeatSecrets()
    print(len(failed_heartbeats_after))
    print(failed_heartbeats_after)
finally:
    # Close the browser window
    driver.quit()

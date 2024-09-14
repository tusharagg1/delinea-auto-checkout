from requests_html import HTMLSession
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

#___________________________________________________INPUT_______________________________________________________________
site = ""  # ex: http://domain.com/SecretServer
authApi = "/oauth2/token"
api = site + "/api/v2"
token = ""
#replace wih local admin creds
session = HTMLSession()


#_____________________________________________GET TOKEN_________________________________________________________________
def GetTotalNumberOfSecrets(token):
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
#_________________________________________________________FILTER___________________________________________________________________
    # Filter rows based on AD Template
    failed_heartbeats = df[
    ((df["secretTemplateName"] == "Active Directory Account") | 
        (df["secretTemplateName"] == "ATCO Active Directory") | 
            (df["secretTemplateName"] == "ATCO Active directory account") | 
                (df["secretTemplateName"] == "ATCO Active directory account -NO Heartbeat") |
                    (df["secretTemplateName"] == "ATCO Active directory account RDP/PUTTY") | 
                        (df["secretTemplateName"] == "ATCO Active directory account-linux") |
                            (df["secretTemplateName"] == "ATCO Active directory account-linux-Ansible-Heartbeat") | 
                                (df["secretTemplateName"] == "ATCO RSA POC Domain Controllers Active Directory Account")) 
    &
    # Filter rows based on lastHeartBeatStatus 
    ((df["lastHeartBeatStatus"] == "Failed") | 
        (df["lastHeartBeatStatus"] == "UnableToConnect") | 
            (df["lastHeartBeatStatus"] == "AccountLockedOut") | 
                (df["lastHeartBeatStatus"] == "UnknownError") )
    ]
    
    #saving the data into a csv file
    failed_heartbeats.to_csv("C:/Users/0041TB744/Desktop/git auto/atco-delinea/failedheartbeat.csv")
    length=len(failed_heartbeats)
    df.to_csv("C:/Users/0041TB744/Desktop/git auto/atco-delinea/secret.csv")
    # Display the filtered DataFrame

#___________________________________________________________TEST SECRET 4143____________________________________________________________
    failed_heartbeat1 = failed_heartbeats.iloc[1, 0]
    print(failed_heartbeat1)
    resp1 = requests.get(
        site + "/app#/secrets/checkout/4143", headers=headers
    )
    print(resp1)
    failed_heartbeat4143=4143
    # Check if the response is valid
    if resp1.status_code == 200:
        # Get the page content using requests-html
        r = session.get(site + "/app#/secrets/checkout/4143", headers=headers)
        # Render JavaScript (this will process the JavaScript on the page)
        
#_____________________________________USING HTML SESSION{code inside test block_______________________________________________________________________________        
        #------------------Failing here----------------------------------------
#        r.html.render()
#        # Find the button by its ID and click it
#        button = r.html.find('#checkout-button', first=True)
#        if button:
#            button.click()
#            print(f"Clicked the checkout button for {failed_heartbeat4143}")
#        else:
#            print(f"Checkout button not found for {failed_heartbeat4143}")
#    else:
#        print(f"Failed to get a valid response for {failed_heartbeat4143}")


#_______________________________________________________________FOR THE WHOLE DATA FRAME___________________________________________
#For looping through   
   
    # Loop through the rows in the DataFrame
    for i in range(length):
        failed_heartbeat1 = failed_heartbeats.iloc[i, 0]
        print(f"Failed heartbeat {i + 1}: {failed_heartbeat1}")
    
        # Make the request using the current failed heartbeat
        resp = requests.get(
            f"{site}/app#/secrets/checkout/{failed_heartbeat1}", headers=headers
         )
            # Build the URL for the current heartbeat
        url = f"{site}/app#/secrets/checkout/{failed_heartbeat1}"


#_________________________________Selenium{inside looping}__________________________________________________________________________________________    
    # Use Selenium to navigate to the page
#    driver.get(url)
    
    # Wait for the page to load and the button to become clickable
#    try:
        # Locate and click the button with id "checkout-button"
#        checkout_button = driver.find_element(By.ID, "checkout-button")
#        checkout_button.click()
 #       print(f"Clicked on checkout button for {failed_heartbeat}")
 #   except Exception as e:
  #      print(f"Failed to click checkout button for {failed_heartbeat}: {e}")
#        print(resp)


    
    #failed_heartbeats to perform checkout-checkin
    #id="checkout-button"
    #id="checkout-approval-options-menu-button" 
    
# Example usage
GetTotalNumberOfSecrets(token)


# Close the session
session.close()
 

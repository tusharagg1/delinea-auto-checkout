import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

site = os.getenv("API_SITE")
authApi = "/oauth2/token"
api = site + "/api/v2"
token = os.getenv("API_TOKEN")


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
        "Active Directory Account",
        "ATCO Active Directory",
        "ATCO Active directory account",
        "ATCO Active directory account -NO Heartbeat",
        "ATCO Active directory account RDP/PUTTY",
        "ATCO Active directory account-linux",
        "ATCO Active directory account-linux-Ansible-Heartbeat",
        "ATCO RSA POC Domain Controllers Active Directory Account",
    ]

    failed_heartbeats = df[
        df["secretTemplateName"].isin(secret_templates)
        & df["lastHeartBeatStatus"].isin(status_filters)
    ]

    return failed_heartbeats["id"]

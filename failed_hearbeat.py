import requests
import pandas as pd

site = ""  # ex: http://domain.com/SecretServer
authApi = "/oauth2/token"
api = site + "/api/v1"
token = ""


def GetTotalNumberOfSecrets(token):
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }
    resp = requests.get(api + "/secrets/", headers=headers)
    if resp.status_code not in (200, 304):
        raise Exception(
            "Error retrieving Secrets. %s %s" % (resp.status_code, resp)
        )
    secrets = resp.json()
    df = pd.DataFrame(secrets["records"])

    # Filter rows where 'lastHeartBeatStatus' is 'Failed'
    failed_heartbeats = df[df["lastHeartBeatStatus"] == "Failed"]

    # Display the filtered DataFrame
    print(failed_heartbeats)


# Example usage
GetTotalNumberOfSecrets(token)
# print("Total number of secrets: %d" % total_secrets)

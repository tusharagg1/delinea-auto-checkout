import http.client
import urllib
import json
import requests
import pandas as pd

site = ""  # ex: http://domain.com/SecretServer
authApi = "/oauth2/token"
api = site + "/api/v1"
token = ""


# REST call to retrieve a secret by ID
# def GetSecret(token, secretId):
#     headers = {
#         "Authorization": "Bearer " + token,
#         "content-type": "application/json",
#     }
#     resp = requests.get(api + "/secrets/" + str(secretId), headers=headers)

#     if resp.status_code not in (200, 304):
#         raise Exception(
#             "Error retrieving Secret. %s %s" % (resp.status_code, resp)
#         )
#     return resp.json()


# # Get secret with ID = 1
# print("Retrieving Secret with id: 1...")
# secret = GetSecret(token, 2090)
# print("Secret Name: " + secret["name"])
# print("Secret ID: " + str(secret["id"]))
# print("Active: " + str(secret["active"]))


def GetTotalNumberOfSecrets(token):
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }
    resp = requests.get(api + "/secrets", headers=headers)
    if resp.status_code not in (200, 304):
        raise Exception(
            "Error retrieving Secrets. %s %s" % (resp.status_code, resp)
        )
    secrets = resp.json()
    df = pd.DataFrame(secrets["records"])

    # if "lastHeartBeatStatus" in df.columns:
    #     # Filter rows where 'lastHeartBeatStatus' is 'Failed'
    failed_heartbeats = df[df["lastHeartBeatStatus"] == "Disabled"]

    # Display the filtered DataFrame
    print(failed_heartbeats)
    # for secret in secrets["records"]:
    #     if secret["lastHeartBeatStatus"] == "Failed":
    #         print(secret)
    # print(len(resp.text))
    # for i in range(20):
    #     print(secrets["records"][i])
    # df = pd.json_normalize(secrets)
    # print(df)
    # # df.to_csv('C:/Users/TusharAggarwal/Downloads/testcsv.csv', index=False)
    # print(df.columns.to_list())
    # return len(
    #     secrets["records"]
    # )  # Assuming the response has a 'records' key with a list of secrets


# Example usage
print("Retrieving total number of secrets...")
GetTotalNumberOfSecrets(token)
# print("Total number of secrets: %d" % total_secrets)

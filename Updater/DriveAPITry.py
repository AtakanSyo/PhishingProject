import json
import requests
import os

def refreshToken(client_id, client_secret, refresh_token):
        params = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
                return r.json()['access_token']
        else:
                return None

access_token = "ya29.a0ARrdaM-8ne6k5kZQD3st41Gdx77dyEBB8PWw1H0o1M90dAB_kMX0cDrGKFrD-ZSvOJXIl080QOxhK9sZ1R1LMLL7IPWGx2neTBykXBCPXs33_Y1XxKCR-FD5QZJvJairmOfp7B74NpJgrNw1NYNjIYWJ40DA"
client_id = "835124988936-dn2kuh7722eb3pqtj8bv51keg32dhs15.apps.googleusercontent.com"
client_secret = "G8oLWgxB1Z6eK-XUmKCQBNpT"
refresh_token = "1//04D8saxjAuFt2CgYIARAAGAQSNwF-L9IrT4CY-uNHVevmQZk9XOm78msbU6njXOsmLLCrMVjvz1jQZngarHoZaluWQ8bZoCVC1sk"

x = refreshToken(client_id, client_secret, refresh_token)

headers = {"Authorization": "Bearer "+x}
para = {
        "key": client_secret,
        'q':"'1EhqcI39sE4uZOl3cxjIhlvv-U8T7P7lT' in parents"
}

r = requests.get(
    "https://www.googleapis.com/drive/v3/files",
    headers=headers,
    params = para,
)

print(r.text)

pWFiles= r.json()['files']

print(pWFiles[0]['name'])

for i in pWFiles:
        print(i['name'])


# If file name with url exists, update.



# if file name with url doesn't exit, create.

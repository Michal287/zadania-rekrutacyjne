from sqlite3 import connect
from requests import request
from requests.auth import HTTPBasicAuth
import json

DOMAIN = "https://recruitment.developers.emako.pl"

f = open('credentials.json')
data = json.load(f)

response = request(
    "POST",
    f"{DOMAIN}/login/aws?grant_type=bearer",
    auth=HTTPBasicAuth(data['username'], data['password']),
)

data = response.json()
print(data['access_token'])


import requests
from requests.auth import HTTPBasicAuth
from urllib.request import urlretrieve
from urllib.parse import parse_qs
import json

# Load Hydra Client Info
file = open('/var/lib/cert-storage/hydraClient.json', 'r')
clientinfo = json.load(file)
file.close()

# Download SSL Certificate
urlretrieve("http://172.24.1.14/download", "cert.pem")

# Set Hydra Client Info
client_id = clientinfo["confClient"]["client_id"]
client_secret = clientinfo["confSecret"]["client_secret"]
redirect_uri = 'https://172.24.1.14/emulator/callback'
scope = ["offline_access"]

# Make initial request to Hydra for 'code'
code_url = "https://172.24.1.14/hydra/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope={}&state=aW90LTVnLWNyZXc".format(client_id, redirect_uri, scope[0])
response = requests.get(code_url, verify="cert.pem")
queryElements=parse_qs(response.text)
code=queryElements['/callback?code'][0]

# Exchange code for a token item (access_token, refresh_token)
token_url = "https://172.24.1.14/hydra/oauth2/token"
payload='grant_type=authorization_code&redirect_uri={}&code={}'.format(redirect_uri, code)
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=payload, headers=headers, verify="cert.pem")

token = response.text

import requests
from requests.auth import HTTPBasicAuth
from urllib.request import urlretrieve
from urllib.parse import parse_qs
import json

file = open('/var/lib/cert-storage/hydraClient.json', 'r')
clientinfo = json.load(file)
file.close()

client_id = clientinfo["confClient"]["client_id"]
client_secret = clientinfo["confSecret"]["client_secret"]
redirect_uri = 'https://172.24.1.14/emulator/callback'
scope = ["offline_access"]

code_url = "https://172.24.1.14/hydra/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope={}&state=aW90LTVnLWNyZXc".format(client_id, redirect_uri, scope[0])
urlretrieve("http://172.24.1.14/download", "cert.pem")

response = requests.get(code_url, verify="cert.pem")
queryElements=parse_qs(response.text)
code=queryElements['/callback?code'][0]

token_url = "https://172.24.1.14/hydra/oauth2/token"
payload='grant_type=authorization_code&redirect_uri={}&code={}'.format(redirect_uri, code)
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=payload, headers=headers, verify="cert.pem")
print(response.text)
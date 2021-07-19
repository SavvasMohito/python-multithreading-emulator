import requests
import json
from urllib.request import urlretrieve
from requests.auth import HTTPBasicAuth
from urllib.parse import parse_qs

# Download SSL Certificate
urlretrieve("http://172.24.1.14/download", "cert.pem")

login_url = "https://172.24.1.14/kratos/self-service/login/api"

# Load Hydra Client Info
file = open('/var/lib/cert-storage/hydraClient.json', 'r')
clientinfo = json.load(file)
file.close()
# Set Hydra Client Info
client_id = clientinfo["confClient"]["client_id"]
client_secret = clientinfo["confSecret"]["client_secret"]
redirect_uri = 'https://172.24.1.14/emulator/callback'
scope = ["offline_access"]

login_payload={}
login_headers = {}

userCredentials=[]
with open('config/registeredUsers.json', 'r') as infile:
    userCredentials = json.load(infile)

for user_identity in userCredentials:
  response = requests.request("GET", login_url, headers=login_headers, data=login_payload, verify="cert.pem")

  json_res = json.loads(response.text)
  id = json_res["id"]

  # Step 2
  url = "https://172.24.1.14/kratos/self-service/login?flow={}".format(id)

  payload = json.dumps({
    "method": "password",
    "password": user_identity["user_password"],
    "password_identifier": user_identity["user_email"]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify="cert.pem")

  json_res = json.loads(response.text)
  session_token = json_res["session_token"]
  #print(response.text)

  # Make initial request to Hydra for 'code'
  code_url = "https://172.24.1.14/hydra/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope={}&state=aW90LTVnLWNyZXc".format(client_id, redirect_uri, scope[0])
  headers = {
    'Authorization': 'Bearer {}'.format(session_token)
  }
  response = requests.get(code_url, headers=headers, verify="cert.pem")
  queryElements=parse_qs(response.text)
  code=queryElements['/callback?code'][0]

  # Exchange code for a token item (access_token, refresh_token)
  token_url = "https://172.24.1.14/hydra/oauth2/token"
  payload='grant_type=authorization_code&redirect_uri={}&code={}'.format(redirect_uri, code)
  headers = {'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Bearer {}'.format(session_token)}
  response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=payload, headers=headers, verify="cert.pem")

  token = response.text
  print(token)
  # add token to mongo with user details 
  # i.e. mongo find(id) push user
  
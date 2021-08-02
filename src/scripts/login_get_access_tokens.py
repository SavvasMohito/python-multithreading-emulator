import json
import os
from urllib.parse import parse_qs
from urllib.request import urlretrieve

import requests
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from requests.auth import HTTPBasicAuth

NGINX_URL=os.getenv('NGINX_HOST_CONFIG')

# Download SSL Certificate
urlretrieve("http://{}/download".format(NGINX_URL), "cert.pem")

# Load Hydra Client Info
file = open('/var/lib/cert-storage/hydraClient.json', 'r')
clientinfo = json.load(file)
file.close()

# Set Hydra Client Info
client_id = clientinfo["confClient"]["client_id"]
client_secret = clientinfo["confSecret"]["client_secret"]
redirect_uri = 'https://{}/emulator/callback'.format(NGINX_URL)
scope = ["offline_access"]

# Set URLs
code_url = "https://{}/hydra/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope={}&state=aW90LTVnLWNyZXc".format(NGINX_URL, client_id, redirect_uri, scope[0])
login_url = "https://{}/kratos/self-service/login/api".format(NGINX_URL)
token_url = "https://{}/hydra/oauth2/token".format(NGINX_URL)

# Load registered users' info in userCredentials list
userCredentials=[]
with open('config/registeredUsers.json', 'r') as infile:
    userCredentials = json.load(infile)

localClient = MongoClient(
    "mongodatabasehost",
    27017,
    serverSelectionTimeoutMS=10,
    connectTimeoutMS=20000,
)
# Check connectivity
try:
  localClient.server_info()
except ServerSelectionTimeoutError:
  print("local server is down.")
  exit()
dbCollection = localClient["iotUsers"]["users"]   

storeCredentials = []

for user_identity in userCredentials:
  
  # Get Login Flow from Kratos
  response = requests.request("GET", login_url, verify="cert.pem")
  json_res = json.loads(response.text)
  action_url = json_res['ui']['action']

  # Submit Login form to Kratos
  payload = json.dumps({
    "method": "password",
    "password": user_identity["user_password"],
    "password_identifier": user_identity["user_email"]
  })

  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", action_url, headers=headers, data=payload, verify="cert.pem")

  json_res = json.loads(response.text)
  session_token = json_res["session_token"]

  # Make initial request to Hydra for 'code'
  headers = {
    'Authorization': 'Bearer {}'.format(session_token)
  }
  response = requests.get(code_url, headers=headers, verify="cert.pem")
  queryElements=parse_qs(response.text)
  # redirect on hlogin,hconsent requires changes
  # device-manager crash here , fixed with retry (axios post issue) 
  code=queryElements['/callback?code'][0]

  # Exchange code for a token item (access_token, refresh_token)
  payload='grant_type=authorization_code&redirect_uri={}&code={}'.format(redirect_uri, code)
  headers = {'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Bearer {}'.format(session_token)}
  response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=payload, headers=headers, verify="cert.pem")

  token = json.loads(response.text)
  
  # Add registered user in list
  storeCredentials.append({
    "user_token":token["access_token"],
    "user_id":json_res['identity']['id']
  })

  # Add users and their tokens in mongo
  userEntry = {}
  userFilter={"id":  user_identity["user_id"]}
  userEntry.update({"id":  user_identity["user_id"]})
  userEntry.update({"token":  [token]})
  testDocument = list(dbCollection.find(userFilter))
  if not testDocument:
    dbCollection.insert_one(userEntry)
  else:
    dbCollection.update_one(
      userFilter,
      {"$set":{"token":  [token]}}
      )
  
localClient.close()

# End of registration. Store users in file
with open('config/remoteEmulatorUsers.json', 'w') as outfile:
    json.dump(storeCredentials,outfile, indent=2, sort_keys=True)
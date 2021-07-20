from requests_oauthlib import OAuth2Session
from urllib.request import urlretrieve
import requests
# InsecureTransportError
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This information is obtained upon registration of a new GitHub
client_id = "cc-client"
client_secret = "2WJo0S-Nn~QmKRMLeu5m-MbxbM"
authorization_base_url = 'https://172.24.1.14/hydra/oauth2/auth'
token_url = 'https://172.24.1.14/hydra/oauth2/token'

# Retrieve ssl certificate from the http /download endpoint
urlretrieve("http://172.24.1.14/download", "cert.pem")
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#redirect_uri=https://172.24.1.14/userTokens
# replace userTokens with device-manager internal endpoint OR implement login flow
state="aW90LTVnLWNyZXc"
response_type="code"
hydra_req_url="https://172.24.1.14/hydra/oauth2/auth?client_id=cc-client&redirect_uri=https://172.24.1.14/userTokens&response_type=code&scope=offline_access&state=aW90LTVnLWNyZXc"
response = requests.get(hydra_req_url, data="", headers=headers, verify="cert.pem")
hydraClient = OAuth2Session(client_id, state=state)
token = hydraClient.fetch_token(token_url, client_secret=client_secret, authorization_response=response_type)
# MismatchingStateError (mismatching_state) CSRF Warning! State not equal in request and response.
exit()

# from flask import Flask, request, redirect, session, url_for
# from flask.json import jsonify
# flow starts with "http://172.24.1.14/hydra/oauth2/auth?client_id=cc-client&redirect_uri=https://172.24.1.14/userTokens&response_type=code&scope=offline_access&state=aW90LTVnLWNyZXc"
# @app.route("/login")
# def login():
#     github = OAuth2Session(client_id)
#     authorization_url, state = github.authorization_url(authorization_base_url)

#     # State is used to prevent CSRF, keep this for later.
#     session['oauth_state'] = state
#     return redirect(authorization_url)

# @app.route("/callback")
# def callback():
#     github = OAuth2Session(client_id, state=session['oauth_state'])
#     token = github.fetch_token(token_url, client_secret=client_secret,
#                                authorization_response=request.url)

#     return jsonify(github.get('https://api.github.com/user').json())




# {
#   "confClient": {
#     "client_id": "cc-client",
#     "grant_types": [
#       "authorization_code",
#       "refresh_token"
#     ],
#     "redirect_uris": [
#       "https://172.24.1.14/userTokens"
#     ],
#     "response_types": [
#       "code"
#     ],
#     "scope": "offline_access"
#   },
#   "confSecret": {
#     "client_secret": "2WJo0S-Nn~QmKRMLeu5m-MbxbM"
#   }
# }

#             const client = new AuthorizationCode({
#               client: {
#                 id: confClient.client_id,
#                 secret: confSecret.client_secret,
#               },
#               auth: {
#                 tokenHost: 'http://172.24.1.14/hydra',
#                 tokenPath: '/oauth2/token',
#                 authorizePath: '/oauth2/auth',
#               }
#             });
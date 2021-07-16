import requests
from urllib.request import urlretrieve
from requests_oauthlib import OAuth2Session
from urllib.request import urlretrieve
from urllib.parse import parse_qs
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


code_url = "https://172.24.1.14/hydra/oauth2/auth?client_id=cc-client&redirect_uri=https://172.24.1.14/emulator/callback&response_type=code&scope=offline_access&state=aW90LTVnLWNyZXc"
urlretrieve("http://172.24.1.14/download", "cert.pem")

response = requests.get(code_url, verify="cert.pem")
queryElements=parse_qs(response.text)
code=queryElements['/callback?code'][0]
print(code)
client_id = 'cc-client'
client_secret = '0~Ddb0H4QmmWTFJJX6rGE12SNA'
redirect_uri = 'https://172.24.1.14/emulator/callback'
scope = ["offline_access"]

# oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
#                           scope=scope)

# token = oauth.fetch_token(
#         'https://172.24.1.14/hydra/oauth2/token',
#         authorization_response="https://172.24.1.14/emulator/callback", code=code, verify=False) 

token_url = "https://172.24.1.14/hydra/oauth2/token"
payload='grant_type=authorization_code&redirect_uri=https://172.24.1.14/emulator/callback&code={}'.format(code)
headers = {'Content-Type': 'application/x-www-form-urlencoded',
						'Authorization': 'Basic Y2MtY2xpZW50OjB+RGRiMEg0UW1tV1RGSkpYNnJHRTEyU05B'}
response = requests.post(token_url, data=payload, headers=headers, verify="cert.pem")
print(response.text)
import requests
from urllib.request import urlretrieve
from requests_oauthlib import OAuth2Session
from urllib.request import urlretrieve
from urllib.parse import parse_qs

code_url = "https://172.24.1.14/hydra/oauth2/auth?client_id=cc-client&redirect_uri=https://172.24.1.14/emulator/callback&response_type=code&scope=offline_access&state=aW90LTVnLWNyZXc"
urlretrieve("http://172.24.1.14/download", "cert.pem")

response = requests.get(code_url, verify="cert.pem")
queryElements=parse_qs(response.text)
code=queryElements['/callback?code'][0]
print(code)
client_id = r'cc-clients'
client_secret = r'GQ01TEIYLPG0IXgrBcH3Ks.Ej7'
redirect_uri = 'https://172.24.1.14/emulator/callback'
scope = ["offline_access"]

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scope)

token = oauth.fetch_token(
        'https://172.24.1.14/hydra/oauth2/token',
        authorization_response=code)
print(token)
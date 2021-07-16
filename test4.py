import requests
from urllib.request import urlretrieve

code_url = "http://172.24.1.14/hydra/oauth2/auth?client_id=cc-client&redirect_uri=https://172.24.1.14/emulator/callback&response_type=code&scope=offline_access&state=aW90LTVnLWNyZXc"
urlretrieve("http://172.24.1.14/download", "cert.pem")

response = requests.get(code_url, verify="cert.pem")
print(response.text)
import requests
import json
from urllib.request import urlretrieve


# Download SSL Certificate
urlretrieve("http://172.24.1.14/download", "cert.pem")

url = "https://172.24.1.14/kratos/self-service/login/api"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, verify="cert.pem")

json_res = json.loads(response.text)
id = json_res["id"]
print("hey")

# Step 2
url = "https://172.24.1.14/kratos/self-service/login?flow={}".format(id)

payload = json.dumps({
  "method": "password",
  "password": "testpass12345",
  "password_identifier": "test@iot.crew"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify="cert.pem")

json_res = json.loads(response.text)
session_token = json_res["session_token"]
print(response.text)

# Step 3

#url = "https://172.24.1.14/kratos/self-service/settings/api"
url = "https://172.24.1.14/kratos/self-service/hlogin/api"

payload = {}
headers = {
  'Content-Type': 'application/json',
	'Authorization': 'Bearer {}'.format(session_token)
}

response = requests.request("GET", url, headers=headers, data=payload, verify="cert.pem", allow_redirects=False)
print(response.text)
import json
import secrets
from urllib.request import urlretrieve
import requests
# Download SSL Certificate
urlretrieve("http://172.24.1.14/download", "cert.pem")

registration_url = "https://172.24.1.14/kratos/self-service/registration/api"
headers = {}
payload = {}
with open('config/names.json', 'r') as infile:
    user_names = json.load(infile)
with open('config/config.json', 'r') as infile:
    emulator_settings = json.load(infile)
desired_users=emulator_settings['users']
#print(user_names)
# config/registeredUsers.json exist
# return
# if users already register skip registratiomn and read from file 

userCredentials = []
user_count=0
for name in user_names['names']:
    user_count=user_count+1
    if (desired_users<user_count):
        break
    [first_name, last_name] = name.split(" ")
    user_email = "{}.{}@iot.crew".format(first_name, last_name)
    user_password = secrets.token_urlsafe(16)
    user_name = "{}_{}".format(first_name, last_name)
    

    response = requests.request(
        "GET", registration_url, headers=headers, data=payload, verify="cert.pem")

    json_res = json.loads(response.text)
    action_url = json_res['ui']['action']
    headers = {
    'Content-Type': 'application/json'
    }
    payload = {
        "traits": {
            "email": user_email,
            "name": {
                "first": first_name,
                "last": last_name
            },
            "username": user_name
        },
        "password": user_password,
        "method": "password",
    }
    response = requests.request(
        "POST", 
        action_url, 
        headers=headers, 
        data=json.dumps(payload), 
        verify="cert.pem"
    )

    json_res = json.loads(response.text)
    userCredentials.append({
        "first_name": first_name,
        "last_name": last_name,
        "user_password": user_password,
        "user_email": user_email,
        "user_name": user_name,
        "user_id":json_res['identity']['id']
    })

# end of registration store users details 
with open('config/registeredUsers.json', 'w') as outfile:
    json.dump(userCredentials,outfile, indent=2, sort_keys=True)



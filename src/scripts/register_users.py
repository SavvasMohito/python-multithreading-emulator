import json
import os
import secrets
from urllib.request import urlretrieve

import requests

NGINX_URL=os.getenv('NGINX_HOST_CONFIG')

# Download SSL Certificate
urlretrieve("http://{}/download".format(NGINX_URL), "cert.pem")

registration_url = "https://{}/kratos/self-service/registration/api".format(NGINX_URL)

# Load Users' Info
with open('config/names.json', 'r') as infile:
    user_names = json.load(infile)

# Load Emulator Config
with open('config/config.json', 'r') as infile:
    emulator_settings = json.load(infile)

# Set variables
desired_users=emulator_settings['users']
userCredentials = []
user_count=0

for name in user_names['names']:
    
    # Check for desired users limit
    user_count=user_count+1
    if (desired_users<user_count):
        break

    # Construct User
    [first_name, last_name] = name.split(" ")
    user_email = "{}.{}@iot.crew".format(first_name, last_name)
    user_password = secrets.token_urlsafe(16)
    user_name = "{}_{}".format(first_name, last_name)
    
    # Get Kratos registration flow
    response = requests.request(
        "GET", registration_url, verify="cert.pem")

    json_res = json.loads(response.text)
    action_url = json_res['ui']['action']

    # Submit registration to Kratos
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

    # Add registered user in list
    userCredentials.append({
        "first_name": first_name,
        "last_name": last_name,
        "user_password": user_password,
        "user_email": user_email,
        "user_name": user_name,
        "user_id":json_res['identity']['id']
    })

# End of registration. Store users in file
with open('config/registeredUsers.json', 'w') as outfile:
    json.dump(userCredentials,outfile, indent=2, sort_keys=True)

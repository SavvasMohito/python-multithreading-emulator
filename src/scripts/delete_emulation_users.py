import json

import ory_kratos_client
from ory_kratos_client.api import v0alpha1_api
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Set Kratos Admin endpoint url
configuration = ory_kratos_client.Configuration(
    host="172.24.1.4:4434"
)

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
# Load registered users' info
userCredentials=[]
with open('config/registeredUsers.json', 'r') as infile:
    userCredentials = json.load(infile)

# Enter a context with an instance of the API client
with ory_kratos_client.ApiClient(configuration) as api_client:
    # Delete generated user identities
    api_instance = v0alpha1_api.V0alpha1Api(api_client)
    for user_identity in userCredentials:
        user_id=user_identity["user_id"]
        try:
            # Delete
            api_response = api_instance.admin_delete_identity(id=user_id)
            dbCollection.delete_one({"id":user_id})
        except TypeError as e:
            pass
        except ory_kratos_client.ApiException as e:
            print("Exception when calling V0alpha1Api->admin_create_identity: %s\n" % e)

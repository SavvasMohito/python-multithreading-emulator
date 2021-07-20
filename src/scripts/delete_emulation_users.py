import ory_kratos_client
from ory_kratos_client.api import v0alpha1_api
import json

# Set Kratos Admin endpoint url
configuration = ory_kratos_client.Configuration(
    host="172.24.1.4:4434"
)

# Load registered users' info
userCredentials=[]
with open('config/registeredUsers.json', 'r') as infile:
    userCredentials = json.load(infile)

# Enter a context with an instance of the API client
with ory_kratos_client.ApiClient(configuration) as api_client:
    # Delete generated user identities
    api_instance = v0alpha1_api.V0alpha1Api(api_client)
    for user_identity in userCredentials:
        try:
            # Delete
            api_response = api_instance.admin_delete_identity(id=user_identity["user_id"])
        except TypeError as e:
            pass
        except ory_kratos_client.ApiException as e:
            print("Exception when calling V0alpha1Api->admin_create_identity: %s\n" % e)
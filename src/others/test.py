import time
import ory_kratos_client
from ory_kratos_client.api import admin_api
from ory_kratos_client.exceptions import ApiTypeError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ory_kratos_client.Configuration(
    host="http://172.24.1.4:4434"
)

# Enter a context with an instance of the API client
with ory_kratos_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = admin_api.AdminApi(api_client)
    try:
        api_response = api_instance.list_identities(
            _check_return_type=False
        )
        for identity in api_response:
            pprint(identity["id"])
    except ApiTypeError as e:
        print("Exception when calling AdminApi->list_identities: %s\n" % e)

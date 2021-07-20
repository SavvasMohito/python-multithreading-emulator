import time
import ory_kratos_client
from ory_kratos_client.api import admin_api
from ory_kratos_client.api import v0alpha1_api
from ory_kratos_client.model.json_error import JsonError
from ory_kratos_client.model.identity_list import IdentityList
from ory_kratos_client.model_utils import convert_js_args_to_python_args
from ory_kratos_client.model.admin_create_identity_body import AdminCreateIdentityBody
from ory_kratos_client.model.identity import Identity
from pprint import pprint
import uuid
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ory_kratos_client.Configuration(
    #host = "http://172.24.1.4:4434/"
    host="172.24.1.4:4434"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: oryAccessToken
#configuration = ory_kratos_client.Configuration(
#    access_token = 'YOUR_BEARER_TOKEN'
#)

# Enter a context with an instance of the API client
with ory_kratos_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    #api_instance = admin_api.AdminApi(api_client)
    api_instance = v0alpha1_api.V0alpha1Api(api_client)
    per_page = 100 # int | Items per Page  This is the number of items per page. (optional) if omitted the server will use the default value of 100
    page = 0 # int | Pagination Page (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    # and optional values

    admin_create_identity_body = AdminCreateIdentityBody(
        schema_id='default',
        traits= {
            'email': 'user{}@iot.crew'.format(uuid.uuid4()),
            'name': {'first': 'test{}'.format(uuid.uuid4()), 
            'last': 'test{}'.format(uuid.uuid4())}, 
            'username': 'user{}'.format(uuid.uuid4())
            },
        ) 
        # AdminCreateIdentityBody |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create an Identity
        api_response = api_instance.admin_create_identity(admin_create_identity_body=admin_create_identity_body,_check_return_type=False)
        #pprint(api_response)
    except TypeError as e:
        pass
    except ory_kratos_client.ApiException as e:
        print("Exception when calling V0alpha1Api->admin_create_identity: %s\n" % e)

    try:
        # List Identities
        api_response = api_instance.admin_list_identities(per_page=per_page, page=page,_check_return_type=False)
        #api_response = api_instance.list_identities(per_page=per_page, page=page,_check_return_type=False,state=)
        pprint(api_response)
        for identity in api_response._data_store['value']:
            pprint("id:{},username:{}".format(identity["id"],identity['traits']['username']))
    except ory_kratos_client.ApiException as e:
        print("Exception when calling V0alpha1Api->admin_list_identities: %s\n" % e)

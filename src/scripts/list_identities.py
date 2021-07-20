import ory_kratos_client
from ory_kratos_client.api import v0alpha1_api
from pprint import pprint

# Set Kratos Admin endpoint url
configuration = ory_kratos_client.Configuration(
    host="172.24.1.4:4434"
)

with ory_kratos_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v0alpha1_api.V0alpha1Api(api_client)
    per_page = 100 # int | Items per Page  This is the number of items per page. (optional) if omitted the server will use the default value of 100
    page = 0 # int | Pagination Page (optional) if omitted the server will use the default value of 0
    try:
        api_response = api_instance.admin_list_identities(per_page=per_page, page=page,_check_return_type=False)
        for identity in api_response._data_store['value']:
            pprint("id:{},username:{}".format(identity["id"],identity['traits']['username']))
    except ory_kratos_client.ApiException as e:
        print("Exception when calling V0alpha1Api->admin_list_identities: %s\n" % e)

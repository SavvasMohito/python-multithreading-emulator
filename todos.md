# TODO List for this project

1. <s>Include THIS project as a submodule in the main [oauth2-testing project](https://github.com/SavvasMohito/oauth2-testing/tree/wip/docker-compose) instead of DeviceHive Simulator.</s>

2. <s>Remove [`verify=False`](https://github.com/SavvasMohito/python-device-emulator/blob/8ef3668468029f9fdbd76baef6d0f1909109c780/src/components/device.py#L34) attribute from the device's http request. Instead, we should locate and verify the self-signed ssl certificate while making the https request to the nginx server.</s>

3. <s>Add "user_id" field in the config file and remove "access_token" and "refresh_token" fields which should be retrieved from a mongo connection in the run.py file based on the user_id of the current config file. (This requires access_token expiration handling in the db or while retrieving the access_token in run.py file)</s>

4. <s>Use the Orion endpoint as the device's http request target for data collection (and later use this data in jupyter notebooks for visualization). Also check if additional nginx configuration is needed for this task.</s>

5. Further implementation: ORY Kratos SDK integration needed in order to replicate the following flow for multiple users at the same time:
   1. Register User
   2. Login User
   3. Make initial access token request
   4. Start the device emulation

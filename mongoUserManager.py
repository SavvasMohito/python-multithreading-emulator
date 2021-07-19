"""
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: admin-backend/mongoUserManager.py
# Created Date: Thursday April 8th 2021
# Author: Antonis Vafeas
# Email: antonis.vafeas@bristol.ac.uk
###
MIT License

Copyright (c) 2021 Smart Internet Lab

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ory_kratos_client
from ory_kratos_client.api import v0alpha1_api
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

configuration = ory_kratos_client.Configuration(
    host="172.24.1.4:4434"
)

def updateIdentity(idList):
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
        return
    # remove users before adding ? 
    dbCollection = localClient["iotUsers"]["users"]
    for id in idList:
        userEntry = {}
        userEntry.update({"id": id})
        testDocument = list(dbCollection.find(userEntry))
        if not testDocument:
            dbCollection.insert_one(userEntry)
    localClient.close()

def main(): 
    with ory_kratos_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = v0alpha1_api.V0alpha1Api(api_client)
        per_page = 100 # int | Items per Page  This is the number of items per page. (optional) if omitted the server will use the default value of 100
        page = 0 # int | Pagination Page (optional) if omitted the server will use the default value of 0
        try:
            api_response = api_instance.admin_list_identities(per_page=per_page, page=page,_check_return_type=False)
            idList = [
                identity["id"] for identity in api_response._data_store['value'] if "id" in identity
            ]
            updateIdentity(idList)
            for identity in api_response._data_store['value']:
                pprint("id:{},username:{}".format(identity["id"],identity['traits']['username']))
        except ory_kratos_client.ApiException as e:
            print("Exception when calling V0alpha1Api->admin_list_identities: %s\n" % e)

if __name__ == "__main__":
    main()
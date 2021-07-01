import json
import logging
from pymongo import MongoClient

from components.supervisor import Supervisor


def get_arguments():
    args = False
    try:
        # Read configuration attributes from the config.json file
        file = open('config/config.json', 'r')
        config = json.load(file)
        file.close()

        # access_token = get_access_token(config["user_id"])
        # if access_token is not False:
        args = [config["devices"], config["url"],
                config["device_name"], config["access_token"], config["refresh_token"], config["delay"]]
    except Exception:
        logging.info(Exception)

    return args


def get_access_token(user_id):
    # TODO make a mongo connection
    # retrieve access_token based on given user_id
    # return access_token value
    access_token = False

    try:
        client = MongoClient('172.24.1.5', 27017, serverSelectionTimeoutMS=10,
                             connectTimeoutMS=20000)
        # specify users collection
        # search for users.userID = user_id in the collection
        # set access_token = found user's access_token
    except Exception:
        logging.info(Exception)

    return access_token


def main():
    if get_arguments() is not False:
        supervisor = Supervisor(*get_arguments())
        supervisor.start()


if __name__ == "__main__":
    main()

import json
import logging
import os

from components.supervisor import Supervisor

NGINX_URL = os.getenv('NGINX_HOST_CONFIG')


def get_arguments():
    args = False
    try:
        # Read configuration attributes from the config.json file
        file = open('config/config.json', 'r')
        config = json.load(file)
        file.close()
        args = [
            config["users"],
            config["devices"],
            'https://{}{}'.format(NGINX_URL, config["url"]),
            config["device_name"],
            config["delay"],
            config["minutes_duration"],
            config["tls"]
        ]
    except Exception:
        logging.info(Exception)

    return args


def main():
    # Setup supervisor for all devices for all users
    if get_arguments() is not False:
        print("\nStarting Emulation!")
        supervisor = Supervisor(*get_arguments())
        supervisor.start()


if __name__ == "__main__":
    main()

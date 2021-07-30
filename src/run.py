import json
import logging
import subprocess
from time import time
import os

NGINX_URL=os.getenv('NGINX_HOST_CONFIG')

from components.supervisor import Supervisor
from metrics import save_script_metric

script_list = ['delete_emulation_users.py',
               'register_users.py', 'login_get_access_tokens.py']


def get_arguments():
    args = False
    try:
        # Read configuration attributes from the config.json file
        file = open('config/config.json', 'r')
        config = json.load(file)
        file.close()
        # TODO: change config URL
        args = [
            config["users"],
            config["devices"],
            'https://{}{}'.format(NGINX_URL,config["url"]),
            config["device_name"],
            config["delay"],
        ]
    except Exception:
        logging.info(Exception)

    return args


def main():
    metrics_times = []
    # Run scripts
    for script in script_list:
        print("\nRunning: {}".format(script))
        start_time = time()
        subprocess.call(['python3', "src/scripts/{}".format(script)])
        end_time = time()
        total_time = '{0:.3f}'.format(end_time - start_time)
        save_script_metric({'SCRIPT_NAME': script, 'SCRIPT_TIME': total_time})
        print("Finished in {} seconds.".format(total_time))

    # Setup supervisor for all devices for all users
    if get_arguments() is not False:
        print("\nStarting Emulation!")
        supervisor = Supervisor(*get_arguments())
        supervisor.start()


if __name__ == "__main__":
    main()

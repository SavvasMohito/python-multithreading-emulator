import json
import logging
import subprocess
from time import time

from components.supervisor import Supervisor

script_list=['delete_emulation_users.py', 'register_users.py', 'login_get_access_tokens.py']

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
            config["url"],
            config["device_name"], 
            config["delay"],
        ]
    except Exception:
        logging.info(Exception)

    return args

def main():
    # Run scripts
    for script in script_list:
        print("Running: {}".format(script))
        start_time = time()
        subprocess.call(['python3', "src/scripts/{}".format(script)])
        end_time = time()
        total_time = '{0:.3f}'.format(end_time - start_time)
        print("Finished in {} seconds.".format(total_time))

    # Setup supervisor for all devices for all users 
    if get_arguments() is not False:
        print("Starting Emulation!")
        supervisor = Supervisor(*get_arguments())
        supervisor.start()
        
if __name__ == "__main__":
    main()

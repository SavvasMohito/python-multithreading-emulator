import json
import logging

from components.supervisor import Supervisor

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
    # Setup supervisor for all devices for all users 
    if get_arguments() is not False:
        print("\nStarting Emulation!")
        supervisor = Supervisor(*get_arguments())
        supervisor.start()
        
if __name__ == "__main__":
    main()

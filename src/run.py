import json
import logging

# Import the Supervisor object.
from components.supervisor import Supervisor

# Read and return arguments from the config.json file
def get_arguments():
    args = False
    try:
        # Read configuration attributes from the config.json file
        file = open('config/config.json', 'r')
        config = json.load(file)
        file.close()
        args = [
            config["threads"],
            'https://{}{}'.format(NGINX_URL, config["url"]),
            config["thread_name"],
            config["delay"],
            config["minutes_duration"],
        ]
    except Exception:
        logging.info(Exception)

    return args


def main():
    # Setup supervisor for all threads.
    if get_arguments() is not False:
        print("\nStarting Emulation!")
				# Create and initiate the Supervisor. Also pass the threads' arguments.
        supervisor = Supervisor(*get_arguments())
        supervisor.start()


if __name__ == "__main__":
    main()
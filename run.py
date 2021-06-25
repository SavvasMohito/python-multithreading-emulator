import json

from components.supervisor import Supervisor

# Read configuration attributes from the config.json file
file = open('components/config.json', 'r')
config = json.load(file)
file.close()

args = [config["devices"], config["url"],
        config["device_name"], config["access_token"], config["refresh_token"], config["delay"]]

supervisor = Supervisor(*args)
supervisor.start()

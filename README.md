# Python Threading Device Emulator

This project is inspired by the [DeviceHive Python Device Simulator](https://github.com/devicehive/devicehive-python-device-simulator). It is a simpler device emulator created with Python Threading for testing purposes.

It is recommended to run it using the Docker Container functionallity in order to have all the required libraries and modules automatically installed. It can also be run locally if you do not want to use Docker.

## How to use

1. Build and Run the main [oauth2-testing project](https://github.com/SavvasMohito/oauth2-testing/tree/wip/docker-compose) using Docker. Specific instructions about this step can be found in the project's README.

2. Log in to [kratos-dashboard](https://172.24.1.14/) and go to the userTokens subpage (lock (🔒) symbol on the navigation bar). Make sure the user has an active access_token. If not, click the link shown in the page to get a new one.

3. Copy the User ID found in the userTokens subpage above the access token information and paste it in the `user_id` field in the emulator's config.json file.

4. Run the "Test Data Collector" executable which is used as a test receiver server of the http requests and prints the access token and request body in the terminal.

5. Run the "Device Emulator" executable which starts the emulation based on the configuration found in the config.json file. The devices created send http requests to the Data Collector.

## Configuration

The config.json file contains all the configuration attributes (described below) required for this project to work.

### Available arguments

* `devices` Number of devices to simulate. Default is 1.
* `url` (**required**) Server url in format 'http://server.name/api/rest'. It is used as an HTTP request target by the Device object.
* `device_name` Device name prefix. Default is "iot-device-".
* `user_id` (**required**) The id of the user that we want to run the emulator for. Can be found in kratos-dashboard homepage (after logging in) or in mongo db.
* `delay` Delay between messages in seconds. Default is 1.

### Additional DeviceHive arguments (not implemented)

* `message_limit` Number of messages to be sent before stop. Default is 0 (infinite loop).
* `time_limit` Number of seconds to work before stop. Default is 0 (infinite loop).
* `message_payload` JSON-like message payload. Default is {"key": "value"}.

## Components

### run.py

This is the main executable file which reads the config.json file, creates the Supervisor object, passes it the configuration attributes and finally calls the `Supervisor.start()` function.

### Supervisor

The Supervisor is a single instance object responsible for creating multiple devices (threads) and passing them all the required attributes which are inherited from the run.py file. When the `Supervisor.start()` function is called, a device spawner (main thread) is created and spawns the devices by calling the `Supervisor._create_devices()` private function. When the program stops, the Supervisor shuts down and kills all the created devices (threads).

### Device

The Device object is a Python Thread which is created and controlled by the Supervisor. It inherits all its attributes by the Supervisor including its name which is generated based on the `device_name` prefix string (found in config.json file) followed by a unique integer. The Device is running continuously while its Supervisor is running. The main functionallity is the `Device._send_data()` private function which creates and sends a POST request at the Data Collection API.

## Python Threading

Additional information about Python Threading and how it works can be found in the following links:

* [python docs](https://docs.python.org/3/library/threading.html)
* [video](https://www.youtube.com/watch?v=IEEhzQoKtQU)
* [article](https://realpython.com/intro-to-python-threading/)

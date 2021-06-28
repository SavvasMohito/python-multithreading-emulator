# Python Threading Device Emulator

This project is inspired by the [DeviceHive Python Device Simulator](https://github.com/devicehive/devicehive-python-device-simulator). It is a simpler device emulator created with Python Threading for testing purposes.

It is recommended to run it using the Docker Container functionallity in order to have all the required libraries and modules automatically installed. It can also be run locally if you do not want to use Docker.

## How to use

You can run the two executables via the VS Code debug tab.

1. "Test Data Collector" is used as the receiver server of the http requests and prints the request body in the terminal.

2. "Device Emulator" is running based on the configuration found in the config.json file. The devices created are sending http requests to the Data Collector.

## Configuration

The config.json file contains all the configuration attributes (described below) required for this project to work.

### Available arguments

* `devices` Number of devices to simulate. Default is 1.
* `url` (**required**) Server url in format 'http://server.name/api/rest'. It is used as an HTTP request target by the Device object.
* `delay` Delay between messages in seconds. Default is 1.
* `device_name` Device name prefix. Default is "iot-device-".
* `access_token` Authentication access token.
* `refresh_token` Authentication refresh token.

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

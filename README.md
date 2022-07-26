# Python Multithreading Template

**NOTICE: Please do NOT modify this branch as it represents the clean version of the emulator. Create a new branch instead and start building it for your needs.**

This project is inspired by the [DeviceHive Python Device Simulator](https://github.com/devicehive/devicehive-python-device-simulator). It is a simpler project created with Python Threading for testing purposes and can fit all types of use cases, if configured appropriately.

It is recommended to run it using a Docker Container in order to have all the required libraries and modules automatically installed. It can also be run locally if you do not want to use Docker, but you'll have to manually install all of the project dependencies.

## Configuration

Inside the config folder you can find the config.json file which contains all the configuration attributes (described below) required for this project to work.

Feel free to modify this file based on your project needs. If you do so, please make sure to update the run.py, supervisor.py and thread.py files accordingly.

### Available arguments

* `threads` Number of threads to simulate.
* `thread_name` Thread name prefix.
* `delay` Delay between thread operation in seconds.
* `minutes_duaration` Specifies the duration you want the emulator to run for (in minutes).

## Components

### run.py

This is the main executable file which reads the config.json file, creates the Supervisor object, passes it the configuration attributes and finally calls the `Supervisor.start()` function.

### Supervisor

The Supervisor is a single instance object responsible for creating multiple threads and passing them all the required attributes which are inherited from the run.py file. When the `Supervisor.start()` function is called, a device spawner (main thread) is created and spawns the threads by calling the `Supervisor._create_threads()` private function. When the program stops, the Supervisor shuts down and kills all the created threads.

### Thread

The Thread multi-instance object is a Python Thread which is created and controlled by the Supervisor. It inherits all its attributes by the Supervisor including its name which is generated based on the `thread_name` prefix string (found in config.json file) followed by a unique integer. The Thread is running continuously while its Supervisor is running. Its main functionality should be included in the `run()` function of the thread.py file.

## How to use
There is a default launch configuration for VS Code, which initiates the `run.py` file. This can be used to start the emulator and it is the recommended way for debugging purposes.

Once you have set up the emulator for your needs and you are happy with its functionality, you can just run the `run.py` file externally in order to have better performance compared to the debugging mode.
## Python Threading

Additional information about Python Threading and how it works can be found in the following links:

* [python docs](https://docs.python.org/3/library/threading.html)
* [video](https://www.youtube.com/watch?v=IEEhzQoKtQU)
* [article](https://realpython.com/intro-to-python-threading/)

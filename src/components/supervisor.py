import threading
import time
import logging
import urllib.request

from .device import Device

__all__ = ['Supervisor']
logger = logging.getLogger(__name__)


class Supervisor(object):
    def __init__(self, ndevices, url, device_name, access_token=None, delay=1.):

        self._ndevices = ndevices
        self._device_kwargs = {
            'url': url,
            'access_token': access_token,
            'device_name': device_name,
            'supervisor': self,
            # Maybe add this in the future
            # 'message_payload': message_payload,
            'delay': delay
        }
        self._is_running = False
        self._devices = []

    @property
    def is_running(self):
        return self._is_running

    def _stop(self):
        self._is_running = False
        [d.join() for d in self._devices]

    def _create_devices(self):
        logger.info('Creating Devices...')
        for i in range(self._ndevices):
            device = Device(thread_index=i, **self._device_kwargs)
            device.setDaemon(True)
            device.start()
            self._devices.append(device)

        logger.info('%d device(s) have been created.' % self._ndevices)

    def start(self):
        logger.info('Starting...')
        start_time = time.time()
        self._is_running = True
        try:
            # Retrieve ssl certificate from the http /download endpoint
            urllib.request.urlretrieve(
                "http://172.24.1.14/download", "cert.pem")

            # Create the device spawner thread
            spawner = threading.Thread(
                target=self._create_devices, name='Spawner')
            spawner.setDaemon(True)
            spawner.start()

            while True:
                time.sleep(1)
                alive_devices = len([d for d in self._devices if d.is_alive()])
                logger.info(
                    'Alive devices: %d', alive_devices)

                if not alive_devices:
                    logger.info('No alive devices left.')
                    break

        except KeyboardInterrupt:
            logger.info('Warm shutdown request by Ctrl-C. '
                        'Press again to use force.')
            try:
                self._stop()
            except KeyboardInterrupt:
                logger.info('May the force be with you!')
                raise

        else:
            logger.info('Shutting down...')
            self._stop()

        finally:
            total_time = time.time() - start_time
            logger.info('Total time: %.3f seconds, ', total_time)

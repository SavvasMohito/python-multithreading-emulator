import requests
import logging
import random
import threading
import time

__all__ = ['Device']
logger = logging.getLogger(__name__)
random.seed()


class Device(threading.Thread):

    def __init__(self, supervisor, url, device_name, thread_index,
                 access_token=None, refresh_token=None, delay=1.):
        threading.Thread.__init__(self, name='Device_%s' % thread_index)

        self._supervisor = supervisor
        self._url = url
        self._device_name = device_name + str(thread_index)
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._delay = delay

        self._device = None

    def _send_data(self):
        try:
            requests.post(self._url,
                          json={"device_name": self._device_name, "temp": random.randint(10, 15)}, headers={"Content-Type": "application/json"})
        except(Exception):
            logger.info(Exception)

    def run(self):
        try:
            while self._supervisor.is_running:
                self._send_data()
                time.sleep(self._delay)
        except(Exception):
            logger.info(Exception)

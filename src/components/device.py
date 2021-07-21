import requests
import logging
import random
import threading
import time
import json

__all__ = ['Device']
logger = logging.getLogger(__name__)
random.seed()


class Device(threading.Thread):

    def __init__(self, supervisor, url, device_name, thread_index,
                 access_token=None, delay=1.):
        threading.Thread.__init__(self, name='Device_%s' % thread_index)

        self._supervisor = supervisor
        self._url = url
        self._device_name = device_name + str(thread_index)
        self._access_token = access_token
        self._delay = delay
        self._device = None

    def _send_data(self):
        body = {"id": self._device_name,
                "temp": random.randint(10, 15)}
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(self._access_token)}
        try:
            msg_start = time.time()

            response = requests.post(
                "{}{}".format(self._url, "/v2/entities"), data=json.dumps(body), headers=headers, verify="cert.pem")
            
            if (response.status_code == 200):
                msg_end = time.time()
                msg_time = '{0:.5f}'.format(msg_end - msg_start)
                print("Message successfully sent in {} seconds.".format(msg_time))

            if (response.status_code == 403):
                print("fail")
                response = requests.post(
                        "{}{}".format(self._url, "/getNewToken"), data=json.dumps(body), headers=headers, verify="cert.pem")
                
                # handle token expiration and measure downtime
                down_start = time.time()
                while (True):
                    print("nedhos")
                    response = requests.post(
                        "{}{}".format(self._url, "/getNewToken"), data=json.dumps(body), headers=headers, verify="cert.pem")
                    if (self._access_token != response.text):
                        self._access_token = response.text
                        down_end = time.time()
                        down_time = '{0:.5f}'.format(down_end - down_start)
                        print("Device was down for {} seconds.".format(down_time))
                        break

        except(Exception):
            logger.info(Exception)

    def run(self):
        try:
            while self._supervisor.is_running:
                self._send_data()
                time.sleep(self._delay)
        except(Exception):
            logger.info(Exception)

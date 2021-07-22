import json
import logging
import random
import threading
import time

import requests

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
        self._downtime_start=None

    def _send_data(self):
        body = {"id": self._device_name,
                "temp": random.randint(10, 15)}
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(self._access_token)}
        try:
            msg_start = time.time()

            response = requests.post(
                "{}{}".format(self._url, "/v2/entities"), data=json.dumps(body), headers=headers, verify="cert.pem")
            
            # Message sent successfully
            if (response.status_code == 200):
                # recover from downtime
                if self._downtime_start:
                    down_time_end= time.time()
                    down_time = '{0:.5f}'.format(down_time_end - self._downtime_start)
                    print("Device successfully recovered after {} seconds.".format(down_time))
                    self._downtime_start=None
                msg_end = time.time()
                msg_time = '{0:.5f}'.format(msg_end - msg_start)
                print("Message successfully sent in {} seconds.".format(msg_time))
            elif (response.status_code == 403):
                # tripping here 
                response = requests.post(
                        "{}{}".format(self._url, "/getNewToken"), data=json.dumps(body), headers=headers, verify="cert.pem")
                if (response.status_code == 200):
                    old_access_token=self._access_token
                    self._access_token = response.text
                    headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(self._access_token)}
                    # retry transmission
                    response = requests.post("{}{}".format(self._url, "/v2/entities"), data=json.dumps(body), headers=headers, verify="cert.pem")
                    # try new access token before overwritting previous one
                    if (response.status_code != 200):
                        print("Toekn failed Reason:{}".format(response.text))
                        # race condition in typescript 
                        # 'Access Token invalid or expired.'
                        self._access_token = old_access_token
                else:
                    # set state to downtime
                    self._downtime_start=time.time()
                    # device gets new token that is invalid  
                    print("Packet lost Reason:{}".format(response.text))
            else:
                print("I love debugging")
        except(Exception):
            logger.info(Exception)

    def run(self):
        try:
            while self._supervisor.is_running:
                self._send_data()
                time.sleep(self._delay)
        except(Exception):
            logger.info(Exception)

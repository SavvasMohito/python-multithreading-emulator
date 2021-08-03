import datetime
import json
import logging
import random
import threading
import time

from requests import Session
from metrics import save_device_metric

__all__ = ['Device']
logger = logging.getLogger(__name__)
random.seed()


class Device(threading.Thread):

    def __init__(self, supervisor, url, device_name, thread_index, access_token=None, delay=1., user_id=None):
        threading.Thread.__init__(self, name='Device_%s' % thread_index)

        self._supervisor = supervisor
        self._url = url
        self._device_name = device_name + str(thread_index)
        self._access_token = access_token
        self._delay = delay
        self._device = None
        self._downtime_start = None
        self._user_id = user_id

    def _send_data(self):
        body = {"id": self._device_name,
                "temp": random.randint(10, 15)}
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(self._access_token)}
        try:
            msg_start = time.time()

            response = Session.post("{}{}".format(self._url, "/v2/entities"), data=json.dumps(body), headers=headers, timeout=1)

            # Message sent successfully
            if (response.status_code == 200):
                # recover from downtime
                if self._downtime_start:
                    down_time_end = time.time()
                    down_time = '{0:.5f}'.format(
                        down_time_end - self._downtime_start)
                    #print("Device recovered after {} seconds of downtime.".format(down_time))
                    save_device_metric({'EVENT': 'Device Recovered',
                                        'DURATION': down_time,
                                        'RESPONSE_CODE': response.status_code,
                                        'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
                    self._downtime_start = None
                msg_end = time.time()
                msg_time = '{0:.5f}'.format(msg_end - msg_start)
                #print("Message sent successfully in {} seconds.".format(msg_time))
                save_device_metric({'EVENT': 'Message sent',
                                    'DURATION': msg_time,
                                    'RESPONSE_CODE': response.status_code,
                                    'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
            elif (response.status_code == 403):
                # tripping here
                response = Session.post("{}{}".format(self._url, "/getNewToken"), data=json.dumps(body), headers=headers)
                if (response.status_code == 200):
                    old_access_token = self._access_token
                    self._access_token = response.text
                    headers = {'Content-Type': 'application/json',
                               'Authorization': 'Bearer {}'.format(self._access_token)}
                    # retry transmission
                    response = Session.post("{}{}".format(self._url, "/v2/entities"), data=json.dumps(body), headers=headers)
                    # try new access token before overwritting previous one
                    if (response.status_code != 200):
                        msg = "Token failed. Reason: {}".format(response.text)
                        #print(msg)
                        save_device_metric({'EVENT': msg,
                                            'DURATION': '',
                                            'RESPONSE_CODE': response.status_code,
                                            'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
                        # race condition in typescript
                        # 'Access Token invalid or expired.'
                        self._access_token = old_access_token
                else:
                    # set state to downtime
                    self._downtime_start = time.time()
                    # device gets new token that is invalid
                    msg = "Packet lost. Reason: {}".format(response.text)
                    #print(msg)
                    save_device_metric({'EVENT': msg,
                                        'DURATION': '',
                                        'RESPONSE_CODE': response.status_code,
                                        'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
            else:
                msg = "Error: Unhandled response.status_code"
                #print(msg)
                save_device_metric({'EVENT': msg,
                                    'DURATION': '',
                                    'RESPONSE_CODE': response.status_code,
                                    'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
        except(Exception):
            logger.info(Exception)

    def run(self):
        Session.verify("cert.pem")
        while not self._supervisor.is_setup_complete:
            time.sleep(self._delay)
        try:
            while self._supervisor.is_running:
                self._send_data()
                time.sleep(self._delay)

        except(Exception):
            logger.info(Exception)

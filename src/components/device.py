import datetime
import json
import logging
import random
import threading
import time

from requests import Session,request
import requests
from metrics import save_device_metric

__all__ = ['Device']
logger = logging.getLogger(__name__)
random.seed()


class Device(threading.Thread):

    def __init__(self, supervisor, url, device_name, thread_index, access_token=None, delay=1., user_id=None, tls=True):
        threading.Thread.__init__(self, name='Device_%s' % thread_index)

        self._supervisor = supervisor
        self._url = url
        self._device_name = device_name + str(thread_index)
        self._access_token = access_token
        self._delay = delay
        self._device = None
        self._downtime_start = None
        self._user_id = user_id
        self._registered = False
        self._tls = tls

    def _send_data(self,req_session:Session):
        if not self._registered:
            body = {
                "id": self._device_name,
                "type": "tempsensor",
                "temp": {
                    "type": "Number",
                    "value":random.randint(10, 15)
                }
            }
            req_endpoint="/v2/entities"
            req_method="POST"
        else:
            body = {
                "id": self._device_name,
                "temp": {
                    "value":random.randint(10, 15)
                }
            }
            req_endpoint="/v2/entities/{}/attrs".format(self._device_name)
            req_method="PATCH"

        # body = {"id": self._device_name,
        #         "temp": random.randint(10, 15)}
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(self._access_token),
                   'Fiware-ServicePath': '/{}'.format(self._device_name)}
        try:
            msg_start = time.time()
            
            if self._tls:
                response =req_session.request(req_method,"{}{}".format(self._url, req_endpoint), data=json.dumps(body), headers=headers,timeout=20)
            else:
                response = request(req_method,"{}{}".format(self._url, req_endpoint), data=json.dumps(body), headers=headers, verify="cert.pem",timeout=20)
            # Message sent successfully
            if response.status_code in [200,201,204]:
                self._registered=True
            #if (response.status_code == 200):
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
                save_device_metric({'EVENT': 'NT',
                                    'DURATION': msg_time,
                                    'RESPONSE_CODE': response.status_code,
                                    'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
            elif (response.status_code == 422):
                # device already registered
                self._registered=True
            elif (response.status_code == 403):
                # tripping here
                msg_start = time.time()
                if self._tls:
                    response = req_session.post("{}{}".format(self._url, "/getNewToken"), data=json.dumps(body), headers=headers)
                else:
                    response = requests.post("{}{}".format(self._url, "/getNewToken"), data=json.dumps(body), headers=headers, verify="cert.pem")
                if (response.status_code == 200):
                    old_access_token = self._access_token
                    self._access_token = response.text
                    headers = {'Content-Type': 'application/json',
                               'Authorization': 'Bearer {}'.format(self._access_token),
                               'Fiware-ServicePath': '/{}'.format(self._device_name)}
                    
                    if self._tls:
                        response =req_session.request(req_method,"{}{}".format(self._url, req_endpoint), data=json.dumps(body), headers=headers,timeout=20)
                    else:
                        response =request(req_method,"{}{}".format(self._url, req_endpoint), data=json.dumps(body), headers=headers,timeout=20)
                    # try new access token before overwritting previous one
                    if response.status_code not in [200,201,204]:
                        msg = "Token failed. Reason: {}".format(response.text)
                        #print(msg)
                        save_device_metric({'EVENT': msg,
                                            'DURATION': '',
                                            'RESPONSE_CODE': response.status_code,
                                            'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
                        # race condition in typescript
                        # 'Access Token invalid or expired.'
                        print("major failure device:{} user:{}".format(self._device_name,self._user_id))
                        self._access_token = old_access_token
                    else:
                        msg_end = time.time()
                        msg_time = '{0:.5f}'.format(msg_end - msg_start)
                        #print("Message sent successfully in {} seconds.".format(msg_time))
                        save_device_metric({'EVENT': 'RT',
                                    'DURATION': msg_time,
                                    'RESPONSE_CODE': response.status_code,
                                    'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
                        
                else:
                    # set state to downtime
                    self._downtime_start = time.time()
                    # device gets new token that is invalid
                    msg = "Packet lost. Reason: {}".format(response.text)
                    #print(msg)
                    save_device_metric({'EVENT': 'PL',
                                        'DURATION': '',
                                        'RESPONSE_CODE': response.status_code,
                                        'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
            else:
                msg = "Error: Unhandled response.status_code"
                #print(msg)
                save_device_metric({'EVENT': 'PL',
                                    'DURATION': '',
                                    'RESPONSE_CODE': response.status_code,
                                    'TIMESTAMP': datetime.datetime.now()}, self._device_name, self._user_id)
        except(Exception) as e:
            logger.info("exception: {}".format(e))

    def run(self):
        req_session = Session()
        req_session.verify = 'cert.pem'
        while not self._supervisor.is_setup_complete:
            time.sleep(self._delay)
        try:
            while self._supervisor.is_running:
                self._send_data(req_session)
                time.sleep(self._delay)

        except(Exception):
            logger.info(Exception)

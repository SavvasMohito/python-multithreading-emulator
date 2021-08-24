import json
import logging
import os
import random
import threading
import time
import urllib.request

import numpy as np
from metrics import create_user_metrics_folder, save_script_metric
from pymongo import MongoClient

from .device import Device

NGINX_URL=os.getenv('NGINX_HOST_CONFIG')

__all__ = ['Supervisor']
logger = logging.getLogger(__name__)
logging.basicConfig(filename='supervisor.log', encoding='utf-8', level=logging.INFO)

class Supervisor(object):
    def __init__(self, nusers, ndevices, url, device_name, delay, minutes_duration, tls):

        self._nusers = nusers
        self._ndevices = ndevices
        self._device_kwargs = {
            'url': url,
            'access_token': None,
            'device_name': device_name,
            'supervisor': self,
            # Maybe add this in the future
            # 'message_payload': message_payload,
            'delay': delay,
            'tls': tls
        }
        self._is_running = False
        self._setup_complete= False
        self._devices = []
        self._setup_time= None
        self.minutes_duration = minutes_duration

    # Get access token for each user name
    def get_access_token(self, user_id):
        access_token = False

        try:
            client = MongoClient("mongodb://172.24.1.5:27017/")
            # DB name
            db = client["iotUsers"]
            # Collection
            coll = db["users"]
            x = coll.find_one({"id": user_id})
            if x["token"]:
                access_token = x["token"][0]["access_token"]
        except Exception:
            logging.info(Exception)

        return access_token

    @property
    def is_running(self):
        return self._is_running
    @property
    def is_setup_complete(self):
        return self._setup_complete

    def _stop(self):
        self._is_running = False
        [d.join() for d in self._devices]

    def _create_devices(self):
        logger.info('Creating Devices...')
        userCredentials = []
        j = 0
        population = [0, 1, 2]
        weights = [0.25, 0.5, 0.25]
        ranges = [(6, 11), (12, 20), (21, 24)]
        with open('config/remoteEmulatorUsers.json', 'r') as infile:
            userCredentials = json.load(infile)
        for user_identity in userCredentials:
            user_id = user_identity["user_id"]
            create_user_metrics_folder(user_id)
            self._device_kwargs["access_token"] = user_identity["user_token"]
            for i in range(self._ndevices):
                # TODO: Maybe implement random delay for each device
                #self._device_kwargs["delay"] += random.uniform(0.1, 0.5)
                low_bound=self._device_kwargs["delay"]-self._device_kwargs["delay"]/20
                high_bound=self._device_kwargs["delay"]+self._device_kwargs["delay"]/20
                #self._device_kwargs["delay"] = random.uniform(low_bound,high_bound)
                # switch from fixed delay to poison delay
                # self._device_kwargs["delay"] = np.random.poisson(1//24, 1//6)
                # switch from not working poisson to Savvas' custom poisson
                r = random.choices(population, weights)
                self._device_kwargs["delay"] = 1 / (random.randint(ranges[r[0]][0], ranges[r[0]][1]) / 60)
                device = Device(thread_index=j, **self._device_kwargs, user_id=user_id)
                j = j+1
                device.setDaemon(True)
                device.start()
                self._devices.append(device)

        logger.info('%d device(s) have been created.' % self._ndevices)
        s1 = "s" if self._nusers > 1 else ""
        s2 = "s" if self._ndevices > 1 else ""
        s3 = "s" if self._nusers*self._ndevices > 1 else ""
        print("{} user{} with {} device{} ({} total device{}) have been created.".format(
            self._nusers, s1, self._ndevices, s2, self._nusers*self._ndevices, s3))
        self._setup_complete= True
        self._setup_time=time.time()

    def start(self):
        logger.info('Starting...')
        start_time = time.time()
        self._is_running = True
        try:
            # Retrieve ssl certificate from the http /download endpoint
            urllib.request.urlretrieve(
                "http://{}/download".format(NGINX_URL), "cert.pem")

            # Create the device spawner thread
            devStart = time.time()
            spawner = threading.Thread(
                target=self._create_devices, name='Spawner')
            devEnd = time.time()
            s1 = "s" if self._nusers > 1 else ""
            s2 = "s" if self._ndevices > 1 else ""
            s3 = "s" if self._nusers*self._ndevices > 1 else ""
            devTotal = devEnd - devStart
            print("Access Token distribution for {} user{} with {} device{} ({} total device{}) finished in {} seconds.".format(
                self._nusers, s1, self._ndevices, s2, self._nusers*self._ndevices, s3, devTotal))
            save_script_metric({'SCRIPT_NAME': 'access_token_distribution', 'SCRIPT_TIME': devTotal})
            spawner.setDaemon(True)
            spawner.start()

            while True:
                time.sleep(10)
                alive_devices = len([d for d in self._devices if d.is_alive()])
                logger.info(
                    'Alive devices: %d', alive_devices)

                if not alive_devices:
                    logger.info('No alive devices left.')
                    break
                # Check if 10 minutes elapsed
                if self._setup_time:
                    if time.time()-self._setup_time>self.minutes_duration*60:
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

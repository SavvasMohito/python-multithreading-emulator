import json
import logging
import os
import random
import threading
import time
import urllib.request
from zipfile import ZipFile
from os.path import basename

import numpy as np
from metrics import create_user_metrics_folder
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
            'delay': delay,
            'tls': tls
        }
        self._is_running = False
        self._setup_complete= False
        self._devices = []
        self._setup_time= None
        self._minutes_duration = minutes_duration
        self._sp = [
            "s" if self._nusers > 1 else "",
            "s" if self._ndevices > 1 else "",
            "s" if self._nusers*self._ndevices > 1 else ""
        ]

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
                # switch from fixed delay to Savvas' custom poisson delay
                r = random.choices(population, weights)[0]
                self._device_kwargs["delay"] = 1 / (random.randint(ranges[r][0], ranges[r][1]) / 60)
                device = Device(thread_index=j, **self._device_kwargs, user_id=user_id)
                j = j+1
                device.setDaemon(True)
                device.start()
                self._devices.append(device)

        logger.info('%d device(s) have been created.' % self._ndevices)
        print("{} user{} with {} device{} ({} total device{}) have been created.".format(self._nusers, self._sp[0], self._ndevices, self._sp[1], self._nusers*self._ndevices, self._sp[2]))
        self._setup_complete= True
        self._setup_time=time.time()

    def start(self):
        logger.info('Starting...')
        start_time = time.time()
        self._is_running = True
        try:
            # Retrieve ssl certificate from the http /download endpoint
            urllib.request.urlretrieve("http://{}/download".format(NGINX_URL), "cert.pem")
            # Create the device spawner thread
            devStart = time.time()
            spawner = threading.Thread(target=self._create_devices, name='Spawner')
            devEnd = time.time()
            devTotal = devEnd - devStart
            print("Access Token distribution for {} device{} finished in {} seconds.".format(self._nusers*self._ndevices, self._sp[2], devTotal))
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
                # Check if experiment duration elapsed
                if self._setup_time:
                    if time.time() - self._setup_time>self._minutes_duration * 60:
                        # Create a ZipFile object
                        with ZipFile('./metrics_archive/metrics_{}.zip'.format(str(time.strftime("%Y_%m_%d_%H_%M"))), 'w') as zipObj:
                            # Iterate over all the files in directory
                            for folderName, subfolders, filenames in os.walk("metrics"):
                                for filename in filenames:
                                    # Create complete filepath of file in directory
                                    filePath = os.path.join(folderName, filename)
                                    # Add file to zip
                                    zipObj.write(filePath, basename(filePath))
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

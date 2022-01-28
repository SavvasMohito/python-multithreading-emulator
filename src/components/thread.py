import logging
import random
import threading
import time


__all__ = ['Thread']
logger = logging.getLogger(__name__)
random.seed()


class Thread(threading.Thread):

		# Thread object's constructor.
    def __init__(self, supervisor, thread_name, thread_index, delay=1.):
        threading.Thread.__init__(self, name='Thread_%s' % thread_index)

				# Thread object's attributes. Feel free to add or remove.
        self._supervisor = supervisor
        self._thread_name = thread_name + str(thread_index)
        self._delay = delay

    def run(self):
				# Wait for all the other threads to be initialized.
        while not self._supervisor.is_setup_complete:
            time.sleep(1)

				# Thread's main functionality.
        try:
            while self._supervisor.is_running:
                # Your code goes here!

								# Thread sleeps for specified delay after re-running the code.
								# You can change or disable this in the config/config.json file.
                time.sleep(self._delay)

				# Catch the errors!
        except(Exception):
            logger.info(Exception)
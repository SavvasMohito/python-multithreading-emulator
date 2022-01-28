import logging
import threading
import time

from .thread import Thread


__all__ = ['Supervisor']
logger = logging.getLogger(__name__)
logging.basicConfig(filename='supervisor.log', encoding='utf-8', level=logging.INFO)

class Supervisor(object):
    def __init__(self, nthreads, thread_name, delay, minutes_duration):
       
        # Threads' attributes
        self._thread_kwargs = {
            'thread_name': thread_name,
            'supervisor': self,
            'delay': delay,
        }

        # Supervisor's attributes
        self._threads = []
        self._nthreads = nthreads
        self._is_running = False
        self._setup_complete = False
        self._setup_time = None
        self._minutes_duration = minutes_duration

    # Return Supervisor's running state.
    @property
    def is_running(self):
        return self._is_running

    # Return Supervisor's setup state.
    @property
    def is_setup_complete(self):
        return self._setup_complete

    # Stop all the threads and supervisor.
    def _stop(self):
        self._is_running = False
        [d.join() for d in self._threads]

    # Create the different threads.
    def _create_threads(self):
        logger.info('Creating Threads...')
        for i in range(self._nthreads):
            # Check this part in another branch if you need different delays per thread based on a Poisson-like distribution. 

            # Create the thread object and initiate it.
            thread = Thread(thread_index=i, **self._thread_kwargs)
            thread.start()

            # Append thread in the Supervisor's threads array.
            self._threads.append(thread)


        logger.info('%d thread(s) have been created.' % self._nthreads)
        print('%d thread(s) have been created.' % self._nthreads)
        self._setup_complete = True
        self._setup_time = time.time()

    def start(self):
        logger.info('Starting...')
        start_time = time.time()
        self._is_running = True
        try:
            # Create the thread spawner thread
            spawner = threading.Thread(target=self._create_threads, name='Spawner')
            spawner.setDaemon(True)
            spawner.start()

            while True:
                alive_threads = len([d for d in self._threads if d.is_alive()])
                logger.info(
                    'Alive threads: %d', alive_threads)

                if not alive_threads:
                    logger.info('No alive threads left.')
                    break

                # Check if experiment duration elapsed
                if self._setup_time:
                    if time.time() - self._setup_time > self._minutes_duration * 60:
					    # Stop the supervisor from running
                        break

		# User manual interruption 
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

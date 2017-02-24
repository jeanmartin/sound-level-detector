from queue import Queue
from requests_futures.sessions import FuturesSession
from threading import Thread
from settings import Settings
import json, time, logging

class EventPublisher:
    session = FuturesSession()

    def __init__(self):
        logging.basicConfig(format=Settings.LOG_FORMAT)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(Settings.LOG_LEVEL)

        self.queue = Queue()
        self.start()

    def start(self):
        self.thread = Thread(target=self.worker)
        self.thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        self.thread.start()

    def worker(self):
        while True:
            event = self.queue.get()
            self.__publish(event[0], event[1])
            self.queue.task_done()
            time.sleep(.001)

    def publish(self, event_name, payload):
        self.queue.put([event_name, payload])

    def __publish(self, event_name, payload):
        self.logger.info('Publish event: {0} - {1}'.format(event_name, payload))
        self.session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': event_name, 'payload': payload } }))

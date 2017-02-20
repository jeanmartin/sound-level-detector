from queue import Queue
from requests_futures.sessions import FuturesSession
from threading import Thread
import json, time

class EventPublisher:
    session = FuturesSession()

    def __init__(self):
        self.queue = Queue()
        self.start()

    def start(self):
        self.thread = Thread(target=self.worker)
        self.thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        self.thread.start()

    def worker(self):
        while True:
            event = self.queue.get()
            self.publish(event[0], event[1])
            self.queue.task_done()
            time.sleep(.001)

    def publish(self, event_name, payload):
        self.session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': event_name, 'payload': payload } }))


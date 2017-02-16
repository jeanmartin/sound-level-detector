from queue import Queue
import kraken
from requests_futures.sessions import FuturesSession
import json

class EventPublisher:
    session = FuturesSession()

    def __init__(self):
        self.queue = Queue()

    def start(self):
        while True:
            event = self.queue.get()
            self.publish(event[0], event[1])
            self.queue.task_done()

    def publish(self, event_name, payload):
        self.session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': event_name, 'payload': payload } }))


from threading import Thread
import time, socket

class Heartbeat():
    def __init__(self, service_name, event_publisher):
        self.service_name = service_name
        self.event_publisher = event_publisher
        self.start()

    def start(self):
        thread = Thread(target=self.worker)
        thread.daemon = True
        thread.start()

    def worker(self):
        while True:
            self.event_publisher.publish('heartbeat', { 'service_name': self.service_name, 'hostname': socket.gethostname() })
            time.sleep(60)

from threading import Thread
import time, socket

class Heartbeat():
    def __init__(self, event_publisher):
        self.event_publisher = event_publisher
        self.start()

    def start(self):
        thread = Thread(target=self.worker)
        thread.daemon = True
        thread.start()

    def worker(self):
        while True:
            self.event_publisher.publish('heartbeat', { 'service_name': 'solide', 'hostname': socket.gethostname() })
            time.sleep(60)

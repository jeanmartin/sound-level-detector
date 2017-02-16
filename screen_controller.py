from queue import Queue
from threading import Thread, Lock
import LCD1602
import sys, time

class ScreenController:
    def __init__(self):
        self.lock = Lock()
        LCD1602.init(0x27,1)
        self.queue = Queue()
        self.start()

    def start(self):
        self.thread = Thread(target=self.worker)
        self.thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        self.thread.start()

    def worker(self):
        while True:
            event = self.queue.get()
            self.update_screen(event[0], event[1], event[2])
            self.queue.task_done()
            time.sleep(.001)

    def update_screen(self, column, row, text):
        with self.lock:
            print("updating screen...")
            LCD1602.write(row, column, "                ")
            LCD1602.write(row, column, text)

    def update(self, column, row, text):
        self.queue.queue.clear()
        self.queue.put([column, row, text])


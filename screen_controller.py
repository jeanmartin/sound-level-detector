from queue import Queue
from threading import Thread, Lock
from settings import Settings
import LCD1602
import sys, time

class ScreenController:
    COLUMNS = Settings.SCREEN['columns']
    ROWS = Settings.SCREEN['rows']

    def __init__(self):
        self.lock = Lock()
        LCD1602.init(0x27,1)
        self.queues = []
        # one queue per row
        for row in range(self.ROWS):
            self.queues.append(Queue())
        self.start()

    def start(self):
        self.thread = Thread(target=self.worker)
        self.thread.daemon = True
        self.thread.start()

    def worker(self):
        while True:
            for queue in self.queues:
                event = queue.get()
                self.update_screen(event[0], event[1], event[2])
                self.queue.task_done()
            time.sleep(.001)

    def update_screen(self, column, row, text):
        with self.lock:
            LCD1602.write(row, 0, " " * self.COLUMNS)
            LCD1602.write(row, column, text)

    def validate_column_and_row(self, column, row, text):
        if row+1 > self.ROWS or row < 0:
            print("ScreenController#update: row ({0}) out of range (0-{1})".format(row, self.ROWS-1))
            raise
        if column+len(text) > self.COLUMN or column < 0:
            print("ScreenController#update: column + text length ({0}) out of range (0-{1})".format(column+len(text), self.COLUMNS))
            raise

    def update(self, column, row, text):
        self.validate_column_and_row(column, row, text)
        self.queues[row].queue.clear() # clear all screen updates for this row that are still pending
        self.queues[row].put([column, row, text])

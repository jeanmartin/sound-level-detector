from queue import Queue
from threading import Thread, Lock
from settings import Settings
import LCD1602
import sys, time, logging

class ScreenController:
    COLUMNS = Settings.SCREEN['columns']
    ROWS = Settings.SCREEN['rows']

    def __init__(self):
        logging.basicConfig(format=Settings.LOG_FORMAT)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.lock = Lock()
        LCD1602.init(0x27,1)
        self.queues = []
        # one queue per row
        for row in range(self.ROWS):
            self.queues.append(Queue())
        self.start()

    def start(self):
        self.threads = []
        for row in range(self.ROWS):
            thread = Thread(target=self.worker, args=[row])
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def worker(self, row):
        self.logger.info('Starting queue {0}'.format(row))
        queue = self.queues[row]
        while True:
            event = queue.get()
            self.update_screen(event[0], event[1], event[2])
            queue.task_done()

    def update_screen(self, column, row, text):
        with self.lock:
            self.logger.info('Updating screen [{0}, {1}]: {2}'.format(column, row, text))
            LCD1602.write(0, row, " " * self.COLUMNS)
            LCD1602.write(column, row, text)

    def validate_column_and_row(self, column, row, text):
        if row+1 > self.ROWS or row < 0:
            self.logger.error('row ({0}) out of range (0-{1})'.format(row, self.ROWS-1))
            raise
        if column+len(text) > self.COLUMNS or column < 0:
            self.logger.error('column + text length ({0}) out of range (0-{1})'.format(column+len(text), self.COLUMNS))
            raise

    def update(self, column, row, text):
        self.validate_column_and_row(column, row, text)
        self.queues[row].queue.clear() # clear all screen updates for this row that are still pending
        self.queues[row].put([column, row, text])

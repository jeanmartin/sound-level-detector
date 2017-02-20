from settings import Settings

class Menu():
    OPTIONS = [
        { 'title': 'Threshold', 'key': 'threshold' },
        { 'title': 'Buffer size', 'key': 'buffer_size' }
    ]
    VALUES = {
        'threshold': Settings.INITIAL_THRESHOLD,
        'buffer_size': Settings.INITIAL_BUFFER_SIZE
    }
    VALUE_STEPS = {
        'threshold': 50,
        'buffer_size': 100
    }
    VALUE_RANGES = {
        'threshold': range(0, 1000),
        'buffer_size': range(1,25000)
    }
    CURRENT = 0

    def __init__(self, screen_controller, queue_listen):
        self.screen_controller = screen_controller
        self.queue_listen = queue_listen

    def current_option(self):
        return self.OPTIONS[self.CURRENT]

    def current_value(self):
        key = self.current_option()['key']
        return self.VALUES[key]

    def current_value_text(self):
        return "{0}".format(self.current_value())

    def next_option(self):
        self.CURRENT += 1
        if self.CURRENT >= len(self.OPTIONS):
            self.CURRENT = 0
        self.update_screen()

    def prev_option(self):
        self.CURRENT -= 1
        if self.CURRENT < 0:
            self.CURRENT = len(self.OPTIONS) - 1
        self.update_screen()

    def increase_value(self):
        key = self.current_option()['key']
        step = self.VALUE_STEPS[key]
        self.VALUES[key] += step
        if not self.VALUES[key] in self.VALUE_RANGES[key]:
            self.VALUES[key] = max(self.VALUE_RANGES[key]) + 1 # ranges are weird
        self.queue_listen.put([key, self.VALUES[key]])
        self.update_screen_value()

    def decrease_value(self):
        key = self.current_option()['key']
        step = self.VALUE_STEPS[key]
        self.VALUES[key] -= step
        if not self.VALUES[key] in self.VALUE_RANGES[key]:
            self.VALUES[key] = min(self.VALUE_RANGES[key])
        self.queue_listen.put([key, self.VALUES[key]])
        self.update_screen_value()

    def update_screen(self):
        self.update_screen_option()
        self.update_screen_value()

    def update_screen_option(self):
        self.screen_controller.update(0, 0, self.current_option()['title'])

    def update_screen_value(self):
        self.screen_controller.update(0, 1, self.current_value_text())

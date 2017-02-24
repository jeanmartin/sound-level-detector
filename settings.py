import logging

class Settings:
    INITIAL_THRESHOLD = 500
    INITIAL_BUFFER_SIZE = 5000
    GPIO = {
        'RE_1_CLK': 6,
        'RE_1_DT': 5,
        'RE_2_CLK': 19,
        'RE_2_DT': 13,
        'LED_RED': 21,
        'LED_GREEN': 16,
        'LED_BLUE': 20
    }
    SCREEN = {
        'columns': 16,
        'rows': 2
    }
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = logging.INFO

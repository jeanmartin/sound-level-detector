
class Settings:
    INITIAL_THRESHOLD = 500
    INITIAL_NOISE_LEVEL_BUFFER_SIZE = 5000
    GPIO = {
        'RE_1_CLK': 20,
        'RE_1_DT': 21,
        'RE_2_CLK': 19,
        'RE_2_DT': 16,
        'LED_RED': 17,
        'LED_GREEN': 22,
        'LED_BLUE': 24
    }
    SCREEN = {
        'columns': 16,
        'rows': 2
    }
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

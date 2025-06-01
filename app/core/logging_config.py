import logging
import sys
import logging


class CustomFormatter(logging.Formatter):
    """Собственный форматтер для логгера

    Атрибуты.
    ----------

    violet : str
        Строка, меняющая цвет текста
        в терминале на фиолетовый
    cyan : str
        Строка, меняющая цвет текста
        в терминале на бирюзовый
    yellow : str
        Строка, меняющая цвет текста 
        в терминале на жёлтый
    red : str
        Строка, меняющая цвет текста 
        в терминале на красный
    bold_red : str
        Строка, меняющая цвет текста 
        в терминале на красный, делает его толстым
    reset : str
        Строка, возвращающий цвет текста
        в терминале на стандартный
    format_str : str
        Строка формата.
    FORMATS : dict
        Словарь с форматами в зависимости от уровня
    """

    def __init__(self):
        self.violet:     str = "\033[95m"
        self.cyan:       str = "\033[36m"
        self.yellow:     str = "\x1b[33;20m"
        self.red:        str = "\x1b[31;20m"
        self.bold_red:   str = "\x1b[31;1m"
        self.reset:      str = "\x1b[0m"
        self.format_str: str = "| %(levelname)-8s | %(asctime)-20s | %(name)-6s | %(filename)s:%(lineno)-4d | : %(message)s"
        self.FORMATS: dict = {
            logging.DEBUG:    self.violet   + self.format_str + self.reset,
            logging.INFO:     self.cyan     + self.format_str + self.reset,
            logging.WARNING:  self.yellow   + self.format_str + self.reset,
            logging.ERROR:    self.red      + self.format_str + self.reset,
            logging.CRITICAL: self.bold_red + self.format_str + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = CustomFormatter()

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

import logging
from colorlog import ColoredFormatter

# Set the format for the terminal
console_handler = logging.StreamHandler()
console_formatter = ColoredFormatter(
    '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'INFO': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
    }
)
console_handler.setFormatter(console_formatter)

# Config the log file
file_handler = logging.FileHandler('app.log')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Config the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

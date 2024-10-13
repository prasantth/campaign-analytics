import logging
import os
from datetime import datetime


class Log:
    @staticmethod
    def _get_log_file():
        # Ensure the logs directory exists
        logs_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Create log file based on the current date
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(logs_dir, f"{today}.log")
        return log_file

    @staticmethod
    def setup_logger(level):
        # Setup logger for the app
        log_file = Log._get_log_file()
        logging.basicConfig(
            filename=log_file,
            level=level,
            format='%(asctime)s %(levelname)s: %(filename)s: %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @staticmethod
    def INFO(msg):
        Log.setup_logger(logging.INFO)
        logging.info(msg)

    @staticmethod
    def WARNING(msg):
        Log.setup_logger(logging.WARNING)
        logging.warning(msg)

    @staticmethod
    def ERROR(msg):
        Log.setup_logger(logging.ERROR)
        logging.error(msg)

    @staticmethod
    def DEBUG(msg):
        Log.setup_logger(logging.DEBUG)
        logging.debug(msg)

# Example of how to use this class:
# try:
#     # Your code here
# except Exception as e:
#     Log.ERROR(e)

# Log.INFO("This is an info message")
# Log.WARNING("This is a warning message")
# Log.DEBUG("This is a debug message")

import logging
import os
from datetime import datetime
import inspect


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
    def _get_logger():
        # Get or create a logger
        logger = logging.getLogger("app_logger")
        if not logger.hasHandlers():
            log_file = Log._get_log_file()
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def _get_caller_info():
        # Get the caller's file and function name using the inspect module
        frame = inspect.stack()[2]
        filename = os.path.basename(frame.filename)
        function_name = frame.function
        return filename, function_name

    @staticmethod
    def INFO(msg):
        logger = Log._get_logger()
        filename, function_name = Log._get_caller_info()
        logger.info(f"{filename}: {function_name}: {msg}")

    @staticmethod
    def WARNING(msg):
        logger = Log._get_logger()
        filename, function_name = Log._get_caller_info()
        logger.warning(f"{filename}: {function_name}: {msg}")

    @staticmethod
    def ERROR(msg):
        logger = Log._get_logger()
        filename, function_name = Log._get_caller_info()
        logger.error(f"{filename}: {function_name}: {msg}")

    @staticmethod
    def DEBUG(msg):
        logger = Log._get_logger()
        filename, function_name = Log._get_caller_info()
        logger.debug(f"{filename}: {function_name}: {msg}")

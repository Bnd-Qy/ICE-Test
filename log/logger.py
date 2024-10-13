import logging
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class Logger:
    def __init__(self, log_file=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        if log_file:
            file_handler = logging.FileHandler(log_file,encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def _log(self, level, message, color):
        import inspect
        import os
        
        caller_frame = inspect.currentframe().f_back.f_back
        
        module = inspect.getmodule(caller_frame)
        module_name = module.__name__ if module else "Unknown"
        file_name = os.path.basename(caller_frame.f_code.co_filename)
        line_number = caller_frame.f_lineno
        class_name = caller_frame.f_locals.get('self', None).__class__.__name__ if 'self' in caller_frame.f_locals else ''
        function_name = caller_frame.f_code.co_name
        formatted_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{module_name}] [{file_name}:{line_number}] {message}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colored_message = f"{timestamp} - {color}{logging.getLevelName(level)}{Style.RESET_ALL} - [{class_name}.{function_name}] [{file_name}:{line_number}] - {message}"
        print(colored_message)

    def debug(self, message):
        self._log(logging.DEBUG, message, Fore.CYAN)

    def info(self, message):
        self._log(logging.INFO, message, Fore.GREEN)

    def warning(self, message):
        self._log(logging.WARNING, message, Fore.YELLOW)

    def error(self, message):
        self._log(logging.ERROR, message, Fore.RED)

    def critical(self, message):
        self._log(logging.CRITICAL, message, Fore.MAGENTA + Style.BRIGHT)

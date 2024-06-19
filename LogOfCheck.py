import tkinter as tk
import logging
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path


class LogOfChecking:
    """ This class seems to be a custom logger that logs messages to both a GUI window and a rotating log file.
    The log messages can be of different levels such as info, warning, error, and debug. The rotating log file has
    a maximum size and a backup count, which means when the log file reaches the maximum size, it is closed and a new
    log file is started. The backup count is the number of old log files to keep."""

    def __init__(self, io_inout_log, log_data=None):
        """The constructor method initializes the instance variables.
        # 'io_inout_log' and 'log_data' are parameters passed while creating objects of this class.
        # 'log_var' is a tkinter StringVar object used for GUI text manipulation.
        # 'log_in_window' and 'log_term' are initially set to None."""

        self.io_inout_log = io_inout_log
        self.log_data = log_data
        self.log_var = tk.StringVar()

        self.log_in_window = None
        self.log_term = None

    def set_log_widget(self, log_text_widget):
        """This method sets the 'log_in_window'
        variable to the passed 'log_text_widget' object."""
        self.log_in_window = log_text_widget

    def log_info(self, message):
        """ In this method logs an info level message. It also updates the 'log_data'
        and the 'log_in_window' if it is not None."""
        logging.info(message)
        self.update_log_data(message)
        if self.log_in_window is not None:
            self.log_in_window.update_log_text_widget(message)

    def log_warning(self, message):
        """ Similar to 'log_info', but logs a warning level message."""
        logging.warning(message)
        self.update_log_data(message)
        if self.log_in_window is not None:
            self.log_in_window.update_log_text_widget(message)

    def log_error(self, message):
        """ Similar to 'log_info', but logs an error level message."""
        logging.error(message)
        self.update_log_data(message)
        if self.log_in_window is not None:
            self.log_in_window.update_log_text_widget(message)

    def log_debug(self, message):
        """ Similar to 'log_info', but logs a debug level message."""
        logging.debug(message)
        self.update_log_data(message)
        if self.log_in_window is not None:
            self.log_in_window.update_log_text_widget(message)

    def update_log_data(self, message):
        """ This method updates the 'log_var' with the passed 'message'."""
        log_text = self.log_var.get()
        log_text += f"{message} '\n'"
        self.log_var.set(log_text)

    def log_limit(self):
        """ This method returns a 'RotatingFileHandler' object with a specified log file,
        maximum file size, and backup count."""
        log_file = Path(self.log_data.resource_path('Logs/app_alert_checker.log'))
        return RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)

    def setup_logging(self):
        """ This method sets up the logging by creating a 'StreamHandler' object for stdout.
        It also sets the formatter for the 'StreamHandler' and calls 'setup_logger' method with
        the 'RotatingFileHandler' and 'StreamHandler' objects."""

        self.log_term = logging.StreamHandler(sys.stdout)
        self.log_term.setFormatter(logging.Formatter('%(asctime)s %(levelname)s : %(message)s',
                                                     datefmt='%d-%b-%y %H:%M:%S'))
        self.setup_logger(self.log_limit(), self.log_term)
        return self.log_term

    def setup_logger(self, *handlers):
        """ This method sets up the logger by setting the formatter for each handler in 'handlers'.
            It also adds each handler to the logger and sets the logger level to INFO."""

        formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        for handler in handlers:
            handler.setFormatter(formatter)
            logger = logging.getLogger()
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

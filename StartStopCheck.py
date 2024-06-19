from threading import Thread
import time


class RepeatTimer(Thread):
    """This class with methods starts a stream with a while loop that accepts 2 positional arguments,
    an interval and a function, (the interval is the time interval between checking the program,
    and the function is the command itself that is passed to another console program
    that is in the "EnableTitleButton" folder of this program) and  1 positional argument  message_queue passes -
    this is a message to the event window of the program with the information that "the check is in progress"
    and the counter of the message, i.e. the number of the check."""

    def __init__(self):
        super().__init__()
        self.interval = None
        self.function = None
        self.finished = False
        self.counter = 0

    def run(self):
        self.counter = 1
        while not self.finished:
            self.function()
            time.sleep(self.interval)
            self.counter += 1

    def cancel(self):
        self.finished = True


class StartStopChecking:
    """This class with the start_check method includes a check using the RepeatTimer (self.io_start_ff)
    class by sending it a time interval variable and a method from the Checking module in the Check class, namely
    the alert_checker method, which sends an API request to the site for the variable's status. And the stop_check
    method stops the work of the previous start_check method."""

    def __init__(self, io_data_checking, io_start_stop_log, on_off_check=None):
        """ The constructor method initializes the instance variables. 'io_data_checking', 'io_start_stop_log',
        'io_start_ff', and 'on_off_check' are parameters passed while creating objects of this class, 'timer'
        is initially set to None. """

        self.on_off_check = on_off_check
        self.io_data_checking = io_data_checking
        self.io_start_stop_log = io_start_stop_log

        self.timer = io_data_checking.io_data_repeat

    def start_check(self):
        """  This method initiates a check by creating a timer object using the 'alert_checker' function from
        'io_data_checking'. It sets the time interval for the timer from 'on_off_check.check_time' and starts the timer.
    It then logs an info message and stores a reference to the created timer in 'io_data_checking.io_data_repeat'.
    If any error occurs during this process, it logs an error message."""

        try:

            if self.timer is None or not self.timer.is_alive():

                self.timer = RepeatTimer()
                self.timer.interval = int(self.on_off_check.check_time)
                self.timer.function = self.io_data_checking.alert_checker

                self.timer.start()
                self.io_data_checking.io_data_repeat = self.timer

                self.io_start_stop_log.log_info('Перевірка включена.')

        except:
            self.io_start_stop_log.log_error('Помилка! Щось пішло не так, перевірка не включилась,'
                                             'можливо проблема з даними або потоком.')

    def stop_check(self):
        """This method stops the check if the timer is not None.
        It cancels the timer and logs an info message, else action nothing."""

        if self.timer:
            self.timer.cancel()
            self.timer = None
            self.io_start_stop_log.log_info('Перевірка виключена.')
        else:
            pass

from tkinter import messagebox


class Conditions:
    """This class and all its methods check the program's state configuration, the correctness of cell filling,
        and whether the user's actions are appropriate given the program's current state. Accordingly,
        it notifies the user and logs these actions."""

    def __init__(self, log_data, io_cond_inout, io_conditions=None, on_off_check=None):
        self.io_data_log = log_data
        self.io_cond_inout = io_cond_inout
        self.io_conditions = io_conditions
        self.on_off_check = on_off_check

        self.check_status = None
        self.checkbutton_status = None

    def check_status_start(self):
        """This method starts the check status.
            - If the entered data is not the same as the opened data, it saves the data. If the auto-start status
                is enabled, it logs the information and fills the cells.
            - If the auto-start status is not enabled, it checks the check status.
            - If the check status is enabled, it logs the information.
            - If the check status is not enabled, program process pasess on next method filling_cells which checks
                whether all cells are filled."""

        if self.io_conditions.enter_data() == self.io_conditions.open_data():
            pass
        else:
            self.io_conditions.save_data()

        if self.io_cond_inout.autostart_status:
            if self.check_status:
                self.io_data_log.log_warning("Була натиснута кнопка 'Старт'. Перевірка вже запущена "
                                             "і автоматичний режим перевірки включений.")

                messagebox.showwarning(title="Увага!", message='Перевірка вже запущена і '
                                                               'автоматичний режим перевірки включений.')
            else:
                self.io_data_log.log_info("Була натиснута кнопка 'Старт' (Автоматичний режим виключений).")
                self.filling_cells()
        else:
            if self.check_status:
                self.io_data_log.log_warning("Перевірка вже запущена.")
                messagebox.showwarning(title="Увага!", message='Перевірка вже запущена.')

            else:
                self.filling_cells()

    def check_status_stop(self):
        """This method stops the check status. It reads the auto-start check status from a file.
        - If the auto-start status is enabled, it checks the check status. If the check status is enabled,
            it stops the check, sets the check status to False, and logs the information.
        - If the check status is not enabled, it logs the information and shows a warning message.
        - If the auto-start status is not enabled, it checks the check status. If the check status is enabled,
            it stops the check, sets the check status to False, and logs the information.
        - If the check status is not enabled, it logs the information and shows a warning message."""

        self.io_cond_inout.reading_autostart_check_file()
        if self.io_cond_inout.autostart_status:
            if self.check_status:
                self.on_off_check.stop_check()
                self.check_status = False
            else:
                self.io_data_log.log_warning("Була натиснута кнопка 'Стоп'. Ви зупинили автоматичний режим перевірки. "
                                             "Натисніть кнопку 'Старт' або закрийте та відкрийте програму.")
                messagebox.showwarning(title="Увага!",
                                       message="Була натиснута кнопка 'Стоп'. Ви зупинили автоматичний режим перевірки. "
                                               "Натисніть кнопку 'Старт' або закрийте та відкрийте програму.")
        else:
            if self.check_status:
                self.on_off_check.stop_check()
                self.check_status = False
            else:
                self.io_data_log.log_warning("Ручна і автоматична перевірка не включена, для початку натисніть кнопку 'Старт'.")
                messagebox.showwarning(title="Увага!", message="Ручна і автоматична перевірка не включена, "
                                                                "для початку натисніть кнопку 'Старт'.")

    def filling_cells(self):
        """ This method checks if all the necessary fields are filled. If they are, it calls the time_interval
            next method. If not all the necessary fields are filled, it logs a warning and shows a warning message."""

        if (self.io_conditions.hostname_pc and self.io_conditions.queue_name and
                self.io_conditions.subject_name and self.io_conditions.command_on and
                self.io_conditions.command_off and len(self.io_conditions.check_time) != 0 or ''):
            self.time_interval()
        else:
            self.io_data_log.log_warning("Усі комірки мають бути заповненні.")
            messagebox.showwarning(title='Увага!', message='Усі комірки мають бути заповненні.')

    def time_interval(self):
        """This method gets the check time from the user interface. If the check time is less than 10 seconds,
            it shows a warning message and logs a warning.
           If the check time is not less than 10 seconds, it starts the check and sets the check status to True."""

        self.io_conditions.check_time = self.io_conditions.check_time_spinbox_target.get()
        if int(self.io_conditions.check_time) < 10:
            messagebox.showwarning(title='Увага!',
                                          message="Часовий інтервал має бути не менше < 10 секунд.")
            self.io_data_log.log_warning("Часовий інтервал має бути не менше < 10 секунд.")
        else:
            self.on_off_check.start_check()
            self.check_status = True

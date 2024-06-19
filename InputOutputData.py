import json, sys, os
from tkinter import messagebox
from pathlib import Path


class InOutData:
    """ This class, along with methods, makes it possible to read data from user-filled program cells and write this data
    to files. Also, reading and writing the status of the program's global variables, and the class also has
    an additional method that sets the absolute path to the program's files for the correct conversion of the program
    into an exe file. The status of the checks and the autostart feature are stored in instance variables. The user data
    and the autostart check status are stored in files. The ‘io_data’, ‘io_inout_cond’, ‘io_inout_log’, and
    ‘io_inout_start’ objects are used for input/output operations, conditions, logging,
    and starting operations respectively.
    """

    def __init__(self, io_data, io_inout_cond, io_inout_log, io_inout_start=None):

        """ The constructor method initializes the instance variables.'io_data', 'io_inout_cond', 'io_inout_log', and
        'io_inout_start' are parameters passed while creating objects of this class. 'hostname_pc', 'queue_name',
        'subject_name', 'command_on', 'command_off', 'check_time', 'checkbutton_status', 'check_status', and
        'autostart_status' are initially set to None. 'file_of_saved_command' is set to the path of the user data file
        in the 'Settings' directory. 'autostart_check_file' is set to the path of the autostart check status file in the
        'Settings' directory."""

        self.io_data = io_data
        self.io_inout_cond = io_inout_cond
        self.io_inout_log = io_inout_log
        self.io_inout_start = io_inout_start

        self.hostname_pc = None
        self.queue_name = None
        self.subject_name = None
        self.command_on = None
        self.command_off = None
        self.check_time = None

        self.file_of_saved_command = Path(self.resource_path("Settings/user_data.cfg"))
        self.autostart_check_file = Path(self.resource_path("Settings/status_autostart_check.json"))

        self.checkbutton_status = None
        self.check_status = None
        self.autostart_status = None

    def setup_data(self, io_data):
        """ This method sets up the data by assigning the input to the instance variable
        and calling the enter_data method."""

        self.io_data = io_data
        self.enter_data()

    def enter_data(self):
        """ This method gets the data from the user interface elements and assigns
        them to the instance variables."""

        self.hostname_pc = self.io_data.hostname_pc_entry.get()
        self.queue_name = self.io_data.queue_name_combobox.get()
        self.subject_name = self.io_data.subject_combobox.get()
        self.command_on = self.io_data.command_on_combobox.get()
        self.command_off = self.io_data.command_off_combobox.get()
        self.check_time = self.io_data.check_time_spinbox.get()

        return (self.hostname_pc, self.queue_name, self.subject_name, self.command_on,
                self.command_off, self.check_time)

    def send_data_on_title(self):
        """ This method prepares data to send the enable title object command through the "EnableTitleButton"
        console program in another program called "OnAir"."""

        self.all_data_send_on = (f"{self.hostname_pc}", f"{self.queue_name}",
                                 f"{self.subject_name}", f"{self.command_on}")
        return self.all_data_send_on

    def send_data_off_title(self):
        """ This method prepares data to send the disable title object command through the "EnableTitleButton"
        console program in another program called "OnAir"."""

        self.all_data_send_off = (f"{self.hostname_pc}", f"{self.queue_name}",
                                  f"{self.subject_name}", f"{self.command_off}")
        return self.all_data_send_off

    def save_data(self):
        """ In this method opening method enter_data which get data with cells and saving in file."""
        self.enter_data()
        all_saving_data = [f"{self.hostname_pc}, {self.queue_name}, {self.subject_name}, "
                           f"{self.command_on}, {self.command_off}, {self.check_time}"]

        with open(self.file_of_saved_command, 'w') as writing_info:
            text_write = str(all_saving_data)
            writing_info.write(text_write)

    def open_data(self):
        """ This method opens the file where the user's data is saved. Next function checking condition
        when the file does not exist, it creates a new empty file and program notificated user what this file
        is corrupted or deleted. And if file and data present then data cleared unnecessary characters are removed
        and created new data list for program to read."""

        if not self.file_of_saved_command.exists():
            with open(self.file_of_saved_command, 'x') as file:
                file.write("[' , , , , , ']")

            messagebox.showerror(title='Помилка!',
                                 message="Файл 'user_data' в папці 'Settings' було пошкоджено або видалено. "
                                          "Тепер створено новий порожній файл 'user_data'. "
                                         "Будь ласка, запустіть програму знову.")

            """Need to fix, don't work"""
            # self.io_inout_log.log_error("Файл 'user_data' в папці 'Settings' було пошкоджено або видалено. "
            #                               "Тепер створено новий порожній файл 'user_data'. "
            #                              "Будь ласка, запустіть програму знову.")
        else:
            with (open(self.file_of_saved_command, 'r') as reading_info):
                read_content = reading_info.readline().strip("[]'\n")
                split_content = read_content.split(', ')

                data_list = [args for args in split_content]

                self.hostname_pc_saved, self.queue_name_saved, self.subject_name_saved, \
                self.command_on_saved, self.command_off_saved, self.check_time_saved = data_list

            return (self.hostname_pc_saved, self.queue_name_saved, self.subject_name_saved,
                    self.command_on_saved, self.command_off_saved, self.check_time_saved)

    def saving_status_checkbutton(self):
        """ This method saves the status of the check button into a file. """
        status_value = self.io_data.status_autostart_var.get()
        with open(self.autostart_check_file, 'r') as r_file:
            status_file = json.load(r_file)

            if status_value == status_file["status_autostart"]:
                pass
            else:
                with open(self.autostart_check_file, 'w') as w_file:
                    w_file.write((json.dumps({'status_autostart': status_value})))
                    if status_value:
                        self.io_inout_log.log_info(f"Статус автоперевірки змінено на 'включений'.")
                    else:
                        self.io_inout_log.log_info(f"Статус автоперевірки змінено на 'виключений'.")

    def opening_saved_status_checkbutton(self):
        """ This method reads the saved status of the check button from a file. If check status is True
        then start checking and program notificated user what checking is started, if check status is False
        simply user program to notificated what autocheck is disabled. """

        self.reading_autostart_check_file()
        if self.autostart_status:
            self.io_inout_cond.check_status_start()
            self.io_inout_log.log_info('Автостарт перевірки включений.')
        else:
            self.io_inout_log.log_info('Автостарт перевірки виключений.')

    def reading_autostart_check_file(self):
        """ Opens the file containing the auto-start check status. """

        with open(self.autostart_check_file, 'r') as file:
            data = file.readline()
            if data:
                json_data = json.loads(data)
                if 'status_autostart' in json_data:
                    self.autostart_status = json_data['status_autostart']
                    return self.autostart_status

    def resource_path(self, relative_path):
        """ This method creates an absolute path to the files. After converting this program to an exe file
        with different folders, the program will be able to open additional data files."""
        try:
            """ PyInstaller creates a temp folder and stores path in _MEIPASS."""
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

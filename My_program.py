import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import sys


"""This program checks for an air alert in the state of the country using the site request API if an air alert occurs 
involves a console program (C#) with arguments that send a command to enable/disable the caption object 
in another online live-streaming desktop application. """


class FirstForm:

    def __init__(self, window):
        self.window = window
        self.root = root
        self.window.title("My program")

        self.create_user_info_frame()
        self.create_command_frame()
        self.create_log_text_widget()
        self.enter_data()
        self.open_data()
        self.setup_logging()

        self.checking = False
        self.log_term = None
        self.log_text_widget = None
        self.alerts_status = None
        self.check_time_saved = None
        self.log_text_widget_reference = None
        self.text_handler = None

        self.exe = "ModeTitleButton/ModeTitleButton.exe"

    """Created first label frame which entry cell and 2 cells with Combobox."""
    def create_user_info_frame(self):
        user_info_frame0 = tkinter.LabelFrame(self.window, text="Entering info for sending to OnAir")
        user_info_frame0.grid(row=0, column=0, padx=20, pady=5)

        labels = ["Hostname PC", "Queue name", "Subject"]
        for col, label_text in enumerate(labels):
            label = tkinter.Label(user_info_frame0, text=label_text)
            label.grid(row=0, column=col)

        self.open_data()
        self.hostname_pc_target = tkinter.StringVar(user_info_frame0, value=f"{self.hostname_pc_saved}")
        self.hostname_pc_entry = tkinter.Entry(user_info_frame0, textvariable=self.hostname_pc_target)
        self.hostname_pc_entry.grid(row=1, column=0)

        self.queue_name_target = tkinter.StringVar(user_info_frame0, value=f"{self.queue_name_saved}")
        self.queue_name_combobox = tkinter.ttk.Combobox(user_info_frame0, textvariable=self.queue_name_target,
                                                        values=['FDOnAir1'])
        self.queue_name_combobox.grid(row=1, column=1)

        self.subject_name_target = tkinter.StringVar(user_info_frame0, value=f"{self.subject_name_saved}")
        self.subject_combobox = tkinter.ttk.Combobox(user_info_frame0, textvariable=self.subject_name_target,
                                                     values=['OnAir1.Mirror'])
        self.subject_combobox.grid(row=1, column=2)

        for widget in user_info_frame0.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    """Created a second label frame which have 2 entry cell with combobox and cell spinbox."""
    def create_command_frame(self):

        user_info_frame1 = tkinter.LabelFrame(self.window, text="Command turn on and off titles")
        user_info_frame1.grid(row=2, column=0, padx=10, pady=5)

        labels1 = ['Command turn on', 'Command turn off', 'Check Time (seconds)']
        for col1, label_text1 in enumerate(labels1):
            label1 = tkinter.Label(user_info_frame1, text=label_text1)
            label1.grid(row=2, column=col1)

        self.open_data()
        self.command_on_target = tkinter.StringVar(user_info_frame1, value=f"{self.command_on_saved}")
        self.command_on_combobox = tkinter.ttk.Combobox(user_info_frame1, width=22, textvariable=self.command_on_target,
                                                        values=['Player.SetTitleButton 8 1'])
        self.command_on_combobox.grid(row=3, column=0)

        self.command_off_target = tkinter.StringVar(user_info_frame1, value=f"{self.command_off_saved}")
        self.command_off_combobox = tkinter.ttk.Combobox(user_info_frame1, width=22, textvariable=self.command_off_target,
                                                         values=['Player.SetTitleButton 8 0'])
        self.command_off_combobox.grid(row=3, column=1)

        self.check_time_spinbox_target = tkinter.IntVar(user_info_frame1, value=self.check_time_saved)
        self.check_time_spinbox = tkinter.Spinbox(user_info_frame1, width=5,
                                                  textvariable=self.check_time_spinbox_target, from_=5, to=300)
        self.check_time_spinbox.grid(row=3, column=2)

        self.button_start = tkinter.Button(user_info_frame1, bg='light green', fg='Black', font='Helvetica 11 bold',
                                           text='Start', padx=5, pady=3, command=self.start_check)
        self.button_start.grid(row=4, column=0)

        button_stop = tkinter.Button(user_info_frame1, bg='grey', fg='Black', font='Helvetica 11 bold', text='Stop',
                                     padx=5, pady=3, command=self.stop_check)
        button_stop.grid(row=4, column=1)

        for widget in user_info_frame1.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    """Created thirded label frame text widget which shows log info from actions in this program."""
    def create_log_text_widget(self):
        user_info_frame2 = tkinter.LabelFrame(self.window, text="Event information")
        user_info_frame2.grid(row=3, column=0, padx=10, pady=5)

        self.log_text_widget = scrolledtext.ScrolledText(user_info_frame2, state='disable', wrap=tkinter.WORD)
        self.log_text_widget.grid(row=6, column=0, columnspan=3)

        user_info_frame2.grid_rowconfigure(6, weight=1)
        user_info_frame2.grid_columnconfigure(0, weight=1)

        for widget in user_info_frame2.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    """Getting information from all cells"""
    def enter_data(self):
        self.hostname_pc = self.hostname_pc_entry.get()
        self.queue_name = self.queue_name_combobox.get()
        self.subject_name = self.subject_combobox.get()
        self.command_on = self.command_on_combobox.get()
        self.command_off = self.command_off_combobox.get()
        self.check_time = self.check_time_spinbox.get()

        return self.hostname_pc, self.queue_name

    """Sending arguments with start console program for turn on title object."""
    def send_data_on_title(self):
        self.enter_data()
        self.all_data_send_on = (f"{self.hostname_pc}", f"{self.queue_name}",
                                 f"{self.subject_name}", f"{self.command_on}")
        return self.all_data_send_on

    """Sending arguments with start console program for turn off title object."""
    def send_data_off_title(self):
        self.enter_data()
        self.all_data_send_off = (f"{self.hostname_pc}", f"{self.queue_name}",
                                  f"{self.subject_name}", f"{self.command_off}")
        return self.all_data_send_off

    """Saving information which entered user in all cells."""
    def save_data(self):
        self.enter_data()
        self.all_saving_data = [f"{self.hostname_pc}, {self.queue_name}, {self.subject_name},"
                                f" {self.command_on}, {self.command_off}, {self.check_time}"]

        with open('user_data', 'w') as writing_info:
            self.text_write = str(self.all_saving_data)
            writing_info.write(self.text_write)

    """Opening saved information which a user entered in all cells 
    and this function returned information added in all cells."""
    def open_data(self):

        with open('user_data', 'r') as self.reading_info:
            self.read_content = self.reading_info.readline()
            self.cleaning_content = \
            self.read_content.replace('[', '').replace(']', '').replace("'", "")
            self.split_content = self.cleaning_content.split(', ')

            self.data_list = []

            for args in self.split_content:
                self.data_list.append(args)

            self.hostname_pc_saved = self.data_list[0]
            self.queue_name_saved = self.data_list[1]
            self.subject_name_saved = self.data_list[2]
            self.command_on_saved = self.data_list[3]
            self.command_off_saved = self.data_list[4]
            self.check_time_saved = self.data_list[5]

        return (self.hostname_pc_saved, self.queue_name_saved, self.subject_name_saved,
                self.command_on_saved, self.command_off_saved, self.check_time_saved)

    """Logging information actions."""
    def log_info(self, message):
        logging.info(message)

    """Logging warning actions."""
    def log_warning(self, message):
        logging.warning(message)

    """Logging error actions."""
    def log_error(self, message):
        logging.error(message)

    """limiting file size in bytes and count backup files."""
    def log_limit(self):
        return RotatingFileHandler('app_alert_checker.log', maxBytes=100000, backupCount=3)

    """Formatting log for log file."""
    def setup_logging(self):
        self.log_term = logging.StreamHandler(sys.stdout)
        self.log_term.setFormatter(logging.Formatter('%(asctime)s %(levelname)s : %(message)s',
                                                     datefmt='%d-%b-%y %H:%M:%S'))
        self.setup_logger(self.log_limit(), self.log_term)
        return self.log_term

    """Formatting log for log text widget."""
    def setup_logger(self, *handlers):
        formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        for handler in handlers:
            handler.setFormatter(formatter)
            logger = logging.getLogger()
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

    """A function when pressed button 'Start'."""
    def start_check(self):

        self.enter_data()
        if (self.hostname_pc and self.queue_name and self.subject_name and self.command_on
                and self.command_off and len(self.check_time) != 0 or ''):

            global checking
            checking = True
            self.check_time = self.check_time_spinbox_target.get()
            self.save_data()
            self.alert_checker()

            self.open_data()
            if int(self.check_time) < 10:
                self.stop_check()
                tkinter.messagebox.showwarning(title='Warning',
                                               message="The time interval should not be < 10 seconds.")
                self.log_warning("Time interval should not be < 10 seconds.")

            self.log_info('Pressed button start.')

        else:
            tkinter.messagebox.showwarning(title='Warning', message='All cells must be filled.')
            self.log_warning("Not all cells were filled.")

    """Function of button 'Stop'."""
    def stop_check(self):
        global checking
        checking = False

        self.log_info('Pressed button stop.')

    """Starting window of a program."""
    def run(self):
        self.window.mainloop()

    """API Requesting with time interval and start console program with arguments when changed value in a site."""
    def alert_checker(self):

        if checking:

            with open('api_key0', 'r') as self.api_file0:
                self.api_key0 = self.api_file0.read()

            self.value_id = 1
            self.url = f"https://api.mysite.com/api/{self.value_id}"

            self.headers = {
                'Accept': 'application/json',
                'Authorization': self.api_key0
            }

            self.response = requests.get(self.url, headers=self.headers)
            self.log_info(f"Response code: {self.response.status_code}")

            if self.response.status_code == 200:
                self.data_list = self.response.json()
                self.new_alerts_status = self.data_list[0]['activeValues']

                if self.new_alerts_status != self.alerts_status:
                    self.alerts_status = self.new_alerts_status

                    self.data = self.data_list[0]
                    self.value_name = self.data.get('valueName')
                    self.log_info(f"Checking value: {self.value_name}.")

                    if len(self.alerts_status) == 0:
                        self.start_command = subprocess.run([self.exe] + list(self.send_data_off_title()))
                        self.log_info(self.start_command)

                        self.log_info('There is no air alarm. Turning off a title.')

                    else:
                        for value in self.alerts_status:
                            self.key = value['type']

                            if self.key == 'True':
                                self.start_command = subprocess.run([self.exe] + list(self.send_data_on_title()))
                                self.log_info(self.start_command)

                                self.log_info('Air Alert!Turning on a title.')
                            else:
                                pass
            else:
                self.log_error(f'Error in request: {self.response.status_code}. Check your Internet connection.')

            self.window.after((int(self.check_time) * 1000), self.alert_checker)

        else:
            self.log_info('Checking is stopped.')


if __name__ == "__main__":
    root = tkinter.Tk()
    app = FirstForm(root)
    app.run()
    checking = True
    root.mainloop()

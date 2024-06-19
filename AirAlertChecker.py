import queue
import tkinter as tk
import time, json

from tkinter import ttk, scrolledtext, PhotoImage, messagebox
from Cryption import EncryptionDescription

from InputOutputData import InOutData
from LogOfCheck import LogOfChecking
from Checking import Check
from CheckingСonditions import Conditions
from StartStopCheck import StartStopChecking, RepeatTimer


class FirstForm:
    """This class  to be used for creating a GUI window for an application called “Air Alert Checker 2.0”. The window
    contains a user info frame, a command frame, a log text widget, and an autostart check frame. The status of
    a checkbutton is loaded when the form is created. The ‘io_data_inout’, ‘io_data_first_form’, ‘io_data_start’,
    ‘io_data_check’, ‘io_data_cond’, and ‘io_data_log’ objects are used for input/output operations, the first form,
    starting operations, checking operations, conditions, and logging respectively."""

    def __init__(self, window=None, io_data_inout=None, io_data_first_form=None, io_data_start=None,
                 io_data_check=None,  io_data_cond=None, io_data_log=None):

        """ The constructor method initializes the instance variables.
        'window', 'io_data_inout', 'io_data_first_form', 'io_data_start', 'io_data_check', 'io_data_cond', and
        'io_data_log' are parameters passed while creating objects of this class.
        The 'window' title is set to "Air Alert Checker 2.0" and the window icon is set by calling the 'window_icon'
        method. The user info frame, command frame, log text widget, and autostart check frame are created by calling
        the respective methods. The status of the checkbutton is loaded by calling the 'load_status_checkbutton' method.
        'status_autostart_var' is set to itself because this variable used in 2 methods create_autostart_check_frame and
        load_status_checkbutton."""

        self.window = window
        self.window.title("Air Alert Checker 2.0")
        self.window.resizable(False, False)
        self.window_icon()

        self.io_data_inout = io_data_inout
        self.io_data_first_form = io_data_first_form
        self.io_data_start = io_data_start
        self.io_data_check = io_data_check
        self.io_data_cond = io_data_cond
        self.io_data_log = io_data_log

        self.create_user_info_frame()
        self.create_command_frame()
        self.create_log_text_widget()
        self.create_autostart_check_frame()
        self.load_status_checkbutton()
        self.hotkeys_bind()

        self.status_autostart_var = self.status_autostart_var
        self.timer = None

    def create_user_info_frame(self):
        """Created first label frame which entry cell and 2 cells with Combobox."""

        user_info_frame0 = tk.LabelFrame(self.window, text="Основні ключі команди для OnAir")
        user_info_frame0.grid(row=0, column=0, padx=20, pady=5)

        labels = ["Ім'я ПК", "Ім'я черги", "Об'єкт"]
        for col, label_text in enumerate(labels):
            label = tk.Label(user_info_frame0, text=label_text)
            label.grid(row=0, column=col)

        self.hostname_pc_target = tk.StringVar(user_info_frame0, value=f"{self.io_data_inout.hostname_pc_saved}")
        self.hostname_pc_entry = tk.Entry(user_info_frame0, textvariable=self.hostname_pc_target)
        self.hostname_pc_entry.grid(row=1, column=0)

        self.queue_name_target = tk.StringVar(user_info_frame0, value=f"{self.io_data_inout.queue_name_saved}")
        self.queue_name_combobox = tk.ttk.Combobox(user_info_frame0, textvariable=self.queue_name_target,
                                                   values=['FDOnAir1'])
        self.queue_name_combobox.grid(row=1, column=1)

        self.subject_name_target = tk.StringVar(user_info_frame0, value=f"{self.io_data_inout.subject_name_saved}")
        self.subject_combobox = tk.ttk.Combobox(user_info_frame0, textvariable=self.subject_name_target,
                                                values=['OnAir1.Mirror'])
        self.subject_combobox.grid(row=1, column=2)

        for widget in user_info_frame0.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def create_command_frame(self):
        """Created a second label frame which have 2 entry cell with combobox and cell spinbox."""

        user_info_frame1 = tk.LabelFrame(self.window, text="Ключі команди вкл/викл титрувального об'єкту та інтервал перевірки")
        user_info_frame1.grid(row=2, column=0, padx=10, pady=5)

        labels1 = ['Ключ вкл.', 'Ключ викл.', 'Інтервал перевірки (секунди)']
        for col1, label_text1 in enumerate(labels1):
            label1 = tk.Label(user_info_frame1, text=label_text1)
            label1.grid(row=2, column=col1)

        self.command_on_target = tk.StringVar(user_info_frame1, value=f"{self.io_data_inout.command_on_saved}")
        self.command_on_combobox = tk.ttk.Combobox(user_info_frame1, width=22, textvariable=self.command_on_target,
                                                   values=['Player.SetTitleButton 8 1'])
        self.command_on_combobox.grid(row=3, column=0)

        self.command_off_target = tk.StringVar(user_info_frame1, value=f"{self.io_data_inout.command_off_saved}")
        self.command_off_combobox = tk.ttk.Combobox(user_info_frame1, width=22, textvariable=self.command_off_target,
                                                    values=['Player.SetTitleButton 8 0'])
        self.command_off_combobox.grid(row=3, column=1)

        self.io_data_inout.check_time_spinbox_target = tk.IntVar(user_info_frame1, value=self.io_data_inout.check_time_saved)
        self.check_time_spinbox = tk.Spinbox(user_info_frame1, width=5,
                                             textvariable=self.io_data_inout.check_time_spinbox_target, from_=10, to=300)
        self.check_time_spinbox.grid(row=3, column=2)

        button_start = tk.Button(user_info_frame1, bg='light green', fg='Black', font='Helvetica 11 bold',
                                 text='Старт', padx=5, pady=3, command=self.io_data_cond.check_status_start)
        button_start.grid(row=4, column=0)

        button_stop = tk.Button(user_info_frame1, bg='light grey', fg='Black', font='Helvetica 11 bold', text='Стоп',
                                padx=5, pady=3, command=self.io_data_cond.check_status_stop)
        button_stop.grid(row=4, column=1)

        for widget in user_info_frame1.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def create_autostart_check_frame(self):
        """Created label with button and checkbutton for function autostart check when start program"""

        user_info_frame2 = tk.LabelFrame(self.window, text='Функція автостарту перевірки')
        user_info_frame2.grid(row=3, column=0, padx=10, pady=0)

        self.status_autostart_var = tk.BooleanVar()
        autostart_on_off = tk.Checkbutton(user_info_frame2, text='Вкл/Викл автостарту перевірки',
                                          variable=self.status_autostart_var, onvalue=True,
                                          offvalue=False)
        autostart_on_off.grid(row=1, column=0)

        button_accept = tk.Button(user_info_frame2, bg='light blue', fg='Black', font='Helvetica 11',
                                  text='ок', padx=5, pady=1,
                                  command=self.io_data_inout.saving_status_checkbutton)
        button_accept.grid(row=1, column=1)

        for widget in user_info_frame2.winfo_children():
            widget.grid_configure(padx=6, pady=6)

    def create_log_text_widget(self):
        """A label has been created in which the events occurring in the program are printed"""

        user_info_frame2 = tk.LabelFrame(self.window, text="Журнал подій")
        user_info_frame2.grid(row=4, column=0, padx=10, pady=5)

        log_text_widget = CustomScrolledText(user_info_frame2, state='disable', wrap=tk.WORD)
        log_text_widget.grid(row=6, column=0, columnspan=3)

        user_info_frame2.grid_rowconfigure(6, weight=1)
        user_info_frame2.grid_columnconfigure(0, weight=1)

        for widget in user_info_frame2.winfo_children():
            widget.grid_configure(padx=7, pady=7)

        self.io_data_log.set_log_widget(log_text_widget)

    def load_status_checkbutton(self):
        """The method that performs the function of opening and loading program settings,
        namely in the cells of the command after the last program launch"""

        if not self.io_data_inout.autostart_check_file.exists():
            with open(self.io_data_inout.autostart_check_file, 'x') as file:
                file.write((json.dumps({"status_autostart": False})))

                io_data_log.log_error("Старий файл 'status_autostart_check' у папці 'Settings'"
                                      "було пошкоджено або видалено. Тепер створений новий файл "
                                      "зі статусом автозапуск вимкнено.")

                messagebox.showerror(title="Помилка!", message="Файл 'status_autostart_check.json' у папці 'Settings' "
                                                            "було пошкоджено або видалено. Тепер створений новий файл "
                                                            "зі статусом автозапуск вимкнено.")
        else:
            json_status = self.io_data_inout.autostart_check_file.read_text()
            load_status = json.loads(json_status)
            status = load_status.get('status_autostart')
            self.status_autostart_var.set(status)

    def confirm_to_exit(self):
        """This method displays a window asking if the user really wants to close the program."""

        ask_exit = messagebox.askyesno(title='Вихід', message='Ви точно хочете закрити програму?')
        if ask_exit:
            if self.io_data_cond.check_status:
                self.io_data_cond.check_status_stop()
            window.destroy()

    def hotkeys_bind(self):
        """ This method binds the 'hotkeys_action' method to the 'Escape', 'F1', and 'F2' keys."""
        window.bind('<Escape>', self.hotkeys_action)
        window.bind('<KeyPress-F1>', self.hotkeys_action)
        window.bind('<KeyPress-F2>', self.hotkeys_action)

    def hotkeys_action(self, event):
        """In this method, the condition of which key to press is checked,
         and the function is assigned to the pressed hot key accordingly."""

        if event.keysym == 'Escape':
            self.confirm_to_exit()
        elif event.keysym == 'F1':
            self.io_data_cond.check_status_start()
        elif event.keysym == 'F2':
            self.io_data_cond.check_status_stop()
        else:
            pass

    def window_icon(self):
        """This method adds an icon to the application window."""

        icon_file = io_data_inout.resource_path('Images/AirAlertChecker.png')
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=icon_file))


class CustomScrolledText(scrolledtext.ScrolledText):
    """This method class displays the event log
    in the create_log_text_widget label method of the FirstForm class"""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def update_log_text_widget(self, message):
        formatted_message = f"{self.get_local_time()} - {message}\n"
        self.configure(state="normal")
        self.insert("end", formatted_message)
        self.see("end")
        self.configure(state="disabled")

    def get_local_time(self):
        local_time = time.localtime()
        format_info = time.strftime("%d-%m-%Y %H:%M:%S", local_time)
        return format_info


if __name__ == "__main__":

    """In this idiom, parameters are accessed from one module to another that are imported into this 
    AirAlertChecker module for data exchange between imported own modules. It also initializes the main Tkinter window. 
    At the beginning of initialization, the "open_data" method is called to load the saved data, and the setup_logging 
    method is also set to ensure the operation of the logging module. There is also a download of the setup_data method 
    that downloads data from the cells so that they can be used in the setup. And finally, 
    the opening_saved_status_checkbutton method is initialized, which loads the automatic check status, 
    whether it is enabled or not, so that the program knows what to do in the future."""

    window = tk.Tk()
    io_log_inout = LogOfChecking(io_inout_log=None)

    io_data_inout = InOutData(io_data=None, io_inout_cond=None, io_inout_log=io_log_inout, io_inout_start=None)
    io_data_inout.open_data()

    io_data_log = LogOfChecking(io_inout_log=None, log_data=io_data_inout)
    io_data_log.setup_logging()

    io_data_crypt = EncryptionDescription(io_data_crypt=io_data_inout, io_data_crypt_log=io_data_log)

    # """This calls of methods for encrypting api key."""
    # io_data_crypt.generate_key()
    # io_data_crypt.encrypt_file()

    io_data_Start_Repeat = RepeatTimer()
    io_data_check = Check(io_data_check_log=io_data_log, io_data_check_crypt=io_data_crypt,
                          io_data_repeat=io_data_Start_Repeat, io_data_checking=io_data_inout)

    io_data_start = StartStopChecking(io_data_checking=io_data_check, io_start_stop_log=io_data_log,
                                      on_off_check=io_data_inout)

    io_data_cond = Conditions(log_data=io_data_log, io_cond_inout=io_data_inout,
                              io_conditions=io_data_inout, on_off_check=io_data_start)

    app = FirstForm(window, io_data_inout=io_data_inout, io_data_cond=io_data_cond,
                    io_data_log=io_data_log)

    io_data_inout.setup_data(app)

    io_data_inout_start = InOutData(io_inout_start=io_data_start, io_inout_cond=io_data_cond,
                                    io_data=None, io_inout_log=io_data_log)

    io_data_inout_start.opening_saved_status_checkbutton()

    window.protocol("WM_DELETE_WINDOW", app.confirm_to_exit)

    window.mainloop()

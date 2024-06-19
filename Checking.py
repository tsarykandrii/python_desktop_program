import requests, subprocess


class Check:
    """ This class is used to check for alerts from a specific API. It logs the region and status of the alerts and runs
    commands based on the alert status. The class is initialized with objects for logging, encryption, and checking data.
    The ‘alert_checker’ method decrypts a file, sends a GET request to the API, and processes the response."""

    def __init__(self, io_data_check_log, io_data_check_crypt, io_data_repeat, io_data_checking=None):
        """ Initializes the Check class with logging, encryption, and checking data."""

        self.io_data_check_log = io_data_check_log
        self.io_data_check_crypt = io_data_check_crypt
        self.io_data_repeat = io_data_repeat
        self.io_data_checking = io_data_checking

        self.alerts_status = None
        self.second_alert_status = None

        self.exe = io_data_checking.resource_path('ModeTitleButton/ModeTitleButton.exe')

    def alert_checker(self):
        """Checks for alerts from a specific API, logs the region and status of the alerts,
        and runs commands based on the alert status."""

        decrypted_info = self.io_data_check_crypt.decrypting_file()

        try:
                # """v1"""
                # self.decrypted_info = os.environ.get('API_KEY0')

                # load_dotenv()
                # self.decrypted_info = os.getenv('API_KEY0')
                # if getattr(sys, 'frozen', False):
                #     self.decrypted_info = sys._MEIPASS
                # load_dotenv(dotenv_path=os.path.join(self.decrypted_info, '.env'))

                # """v2"""
                # exe_file = sys.executable
                # exe_parent = os.path.dirname(exe_file)
                # dotenv_path = os.path.join(exe_parent, '.env')
                #
                # load_dotenv(dotenv_path=dotenv_path)
                # self.decrypted_info = os.getenv('API_KEY0')
                #
                # if self.decrypted_info:
                #     pass
                # else:
                #     self.io_data_check_log.log_error('API key error.')
                #     exit()

            # except KeyError:
            #     self.io_data_check_log.log_error('API key error.')
            #     exit()

            # self.env = dict(os.environ)
            # get_key = self.env.get('API_KEY0')
            #
            # if get_key:
            #      self.env = get_key
            # else:
            #     self.io_data_check_log.log_error('API key error.')
            #     exit()

            region_id = 5
            url = f"https://api.ukrainealarm.com/api/v3/alerts/{region_id}"

            headers = {
                'Accept': 'application/json',
                'Authorization': decrypted_info
            }

            self.response = requests.get(url, headers=headers, timeout=5)

            if self.response.status_code == 200:
                self.io_data_check_log.log_info(f"Іде перевірка ({self.io_data_repeat.counter})")
                data_list = self.response.json()
                new_alerts_status = data_list[0]['activeAlerts']

                if new_alerts_status != self.alerts_status:
                    self.alerts_status = new_alerts_status

                    data = data_list[0]
                    region_name = data.get('regionName')
                    self.io_data_check_log.log_info(f"Регіон: {region_name}.")

                    if len(self.alerts_status) == 0:
                        self.start_command = subprocess.run([self.exe] + list(self.io_data_checking.send_data_off_title()))
                        self.io_data_check_log.log_info(f"Відправлено команду в ПЗ OnAir: {self.io_data_checking.send_data_off_title()}")

                        self.io_data_check_log.log_info("Немає повітряної тривоги. Відправлена команда виключення титрувального об'єкту.")

                    else:
                        for value in self.alerts_status:
                            key = value['type']

                            if key == 'AIR':
                                self.start_command = subprocess.run([self.exe] + list(self.io_data_checking.send_data_on_title()))
                                self.io_data_check_log.log_info(f"Sended command on Forward: {self.io_data_checking.send_data_on_title()}")

                                self.io_data_check_log.log_info("Повітряна тривога! Відправлена команда включення титрувального об'єкту.")
                            else:
                                pass

            elif self.response.status_code == 401:
                self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. Токен API відсутній, '
                                                 f'неправильний, відкликаний або прострочений.')

            elif self.response.status_code == 403:
                self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. Відмовлено в доступі. '
                                                 f'API-ключ відстутній або пошкоджений.')

            elif self.response.status_code == 429:
                self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. '
                                                 f'Забагато запитів на одну хвилину. Має бути не більше 8 запитів. '
                                                 f'Збільшіть час інтервалу перевірки.')

            elif self.response.status_code == 500:
                self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. '
                                                 f'Внутрішня помилка сайту.')

            elif self.response.status_code == 503:
                self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. '
                                             f'Немає відповіді від сайту.')
            else:
                self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. ')

        except requests.exceptions.Timeout:
            self.io_data_check_log.log_error('Час очікування відповіді від сайту закінчився.')

        except requests.ConnectionError:
            self.io_data_check_log.log_info("Відсутнє з'єднання доступу до Інтернет.")

    # def alert_checker_backup(self):
    #     """A fallback method that checks for notifications from a specific API, logs the region and status
    #     of the notifications, and executes commands based on the status of the alert."""
    #
    #     decrypted_key = self.io_data_check_crypt.decrypting_file()
    #
    #     try:
    #         id_region = 16
    #         url = f"https://alerts.com.ua/api/states/{id_region}?short=id&alert"
    #         headers_page = {'X-API-Key': decrypted_key}
    #         self.response_site = requests.get(url, headers=headers_page, timeout=5)
    #
    #         if self.response_site.status_code == 200:
    #             self.io_data_check_log.log_info(f"Іде перевірка ({self.io_data_repeat.counter})")
    #             info = self.response_site.json()
    #             region_info = info.get('state')
    #
    #             if region_info:
    #                 name_state = region_info['name_en']
    #                 first_alert_status = region_info['alert']
    #
    #                 if first_alert_status != self.second_alert_status:
    #                     self.second_alert_status = first_alert_status
    #                     self.io_data_check_log.log_info(f"Регіон: {name_state}")
    #
    #                     if self.second_alert_status:
    #                         self.start_command = subprocess.run([self.exe] + list(self.io_data_checking.send_data_on_title()))
    #                         self.io_data_check_log.log_info(
    #                             f"Sended command on Forward: {self.io_data_checking.send_data_on_title()}")
    #
    #                         self.io_data_check_log.log_info(
    #                         "Повітряна тривога! Відправлена команда включення титрувального об'єкту.")
    #
    #                     else:
    #                         self.start_command = subprocess.run(
    #                             [self.exe] + list(self.io_data_checking.send_data_off_title()))
    #                         self.io_data_check_log.log_info(
    #                             f"Відправлено команду в ПЗ OnAir: {self.io_data_checking.send_data_off_title()}")
    #
    #                         self.io_data_check_log.log_info(
    #                             "Немає повітряної тривоги. Відправлена команда виключення титрувального об'єкту.")
    #
    #             else:
    #                 pass
    #
    #         elif self.response_site.status_code == 403:
    #             self.io_data_check_log.log_error(f'Помилка від сайту: {self.response_site.status_code}. Відмовлено в доступі. '
    #                                             f'API-ключ відстутній або пошкоджений.')
    #
    #         elif self.response_site.status_code == 500:
    #             self.io_data_check_log.log_error(f'Помилка від сайту: {self.response_site.status_code}. '
    #                                             f'Внутрішня помилка сайту.')
    #
    #         elif self.response_site.status_code == 503:
    #             self.io_data_check_log.log_error(f'Помилка від сайту: {self.response_site.status_code}. '
    #                                             f'Немає відповіді від сайту.')
    #
    #         else:
    #             self.io_data_check_log.log_error(f'Помилка від сайту: {self.response.status_code}. ')
    #
    #     except requests.exceptions.Timeout:
    #         self.io_data_check_log.log_error('Час очікування відповіді від сайту закінчився.')
    #
    #     except requests.ConnectionError:
    #         self.io_data_check_log.log_info("Відсутнє з'єднання доступу до Інтернет.")

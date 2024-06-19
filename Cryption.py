import os
from cryptography.fernet import Fernet


class EncryptionDescription:
    """This class is used for encryption and decryption of files. It generates an encryption key, saves it to a file,
    encrypts the content of a file using the saved key, and decrypts the content of the encrypted file using
    the saved key. The class is initialized with objects for encryption and logging data. The ‘generate_key’,
    ‘encrypt_file’, and ‘decrypting_file’ methods perform the key generation, encryption,
    and decryption operations, respectively."""

    def __init__(self, io_data_crypt=None, io_data_crypt_log=None):
        """ Initializes the EncryptionDescription class with encryption and logging data."""

        self.io_data_crypt = io_data_crypt
        self.io_data_crypt_log = io_data_crypt_log

        self.fernet = None
        self.info_decryption = None

        self.key_for_decrypt = self.io_data_crypt.resource_path('Settings/encrypting.key')
        self.encrypt_info = self.io_data_crypt.resource_path('Settings/api.key')

    # def generate_key(self):
    #     """ Generates a new encryption key and saves it to a file."""
    #
    #     key = Fernet.generate_key()
    #
    #     with open(self.key_for_decrypt, 'wb') as keyfile:
    #         keyfile.write(key)
    #
    # def encrypt_file(self):
    #     """ Encrypts the content of a file using the saved encryption key."""
    #
    #     with open(self.key_for_decrypt, 'rb') as keyfile:
    #         key_enc = keyfile.read()
    #
    #     original_content = Fernet(key_enc)
    #
    #     with open(self.encrypt_info, 'rb') as file:
    #         original_info = file.read()
    #
    #     encrypted_info = original_content.encrypt(original_info)
    #
    #     with open(self.encrypt_info, 'wb') as file:
    #         file.write(encrypted_info)

    def decrypting_file(self):
        """ Decrypts the content of the encrypted file using the saved encryption key."""

        try:
         with open(self.key_for_decrypt, 'rb') as keyfile:
             key_dec = keyfile.read()

        except FileNotFoundError:
             self.io_data_crypt_log.log_error('Файл з ключем для розшифрування не знайдено.')
             exit()

        try:
             self.fernet = Fernet(key_dec)

        except ValueError:
             self.io_data_crypt_log.log_error('Ключ для розшифрування не знайдено.')
             exit()


        try:
            with open(self.encrypt_info, 'rb') as keyfile:
                info_dec = keyfile.read()

        except FileNotFoundError:
            self.io_data_crypt_log.log_error('Файл із зашифрованим API ключем не знайдено.')
            exit()
        try:
            self.info_decryption = self.fernet.decrypt(info_dec)

        except ValueError:
            self.io_data_crypt_log.log_error('Помилка API ключа.')
            exit()

        except:
            self.io_data_crypt_log.log_error('API ключ пошкоджений або відсутній.')
            exit()

        return self.info_decryption

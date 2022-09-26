from fernet_wrapper import Wrapper as fw


class Creds:
    """
    A class to store and handle login credentials.

    ...

    Attributes
    ----------
    homeserver : str
        The homeserver for the bot to connect to. Begins with "https://".

    username : str
        The username for the bot to connect as.

    password : str
        The password for the bot to connect with.

    """

    def __init__(self,
                 homeserver,
                 username=None,
                 password=None,
                 login_token=None,
                 access_token=None,
                 session_stored_file='session.txt'):
        """
        Initializes the simplematrixbotlib.Creds class.

        Parameters
        ----------
        homeserver : str
            The homeserver for the bot to connect to. Begins with "https://".

        username : str, optional
            The username for the bot to connect as. This is necessary if password is used instead of login_token.

        password : str, optional
            The password for the bot to connect with. Can be used instead of login_token. One of the password, login_token, or access_token must be provided.

        login_token : str, optional
            The login_token for the bot to connect with. Can be used instead of password. One of the password, login_token, or access_token must be provided.

        access_token : str, optional
            The access_token for the bot to connect with. Can be used instead of password. One of the password, login_token, or access_token must be provided.

        session_stored_file : str, optional
            Location for the bot to read and write device_id and access_token. The data within this file is encrypted and decrypted with the password parameter using the cryptography package. If set to None, session data will not be saved to file.

        """

        self.homeserver = homeserver
        self.username = username
        self.password = password
        self.login_token = login_token
        self.access_token = access_token
        self._session_stored_file = session_stored_file
        self.device_name = "Bot Client using Simple-Matrix-Bot-Lib"
        self.device_id = ""

        if self.password:
            self._key = fw.key_from_pass(self.password)
        elif self.login_token:
            self._key = fw.key_from_pass(self.login_token)
        elif self.access_token:
            self._key = fw.key_from_pass(self.access_token)
        else:
            raise ValueError(
                "password or login_token or access_token is required")

    def session_read_file(self):
        """
        Reads and decrypts the device_id and access_token from file

        """
        if self._session_stored_file:
            try:
                with open(self._session_stored_file, 'r') as f:
                    encrypted_session_data = bytes(f.read()[2:-1], 'utf-8')
                    file_exists = True

            except FileNotFoundError:
                file_exists = False

            if file_exists:
                decrypted_session_data = fw.decrypt(
                    encrypted_session_data,
                    self._key)[3:-2].replace('\'', '').replace(' ',
                                                               '').split(",")

                self.device_id = decrypted_session_data[0]
                self.access_token = decrypted_session_data[1]

                if not self.device_id or not self.access_token or (
                        self.device_id == "") or (self.access_token == ""):
                    raise ValueError(
                        f"Can't load credentials: device ID '{self.device_id}' or access token '{self.access_token}' were not properly saved. "
                        f"Reset your session by deleting {self._session_stored_file} and the crypto store if encryption is enabled."
                    )

        else:
            file_exists = False

        if not file_exists:
            self.device_id = None

    def session_write_file(self):
        """
        Encrypts and writes to file the device_id and access_token.
        """

        if not self._session_stored_file:
            print('device_id and access_token will not be saved')
            return

        if not (self.device_id and self.access_token):
            raise ValueError(
                f"Can't save credentials: missing device ID '{self.device_id}' or access token '{self.access_token}'"
            )
        elif (self.device_id == "") or (self.access_token == ""):
            raise ValueError(
                f"Can't save credentials: empty device ID '{self.device_id}' or access token '{self.access_token}'"
            )

        session_data = str([self.device_id, self.access_token])

        encrypted_session_data = fw.encrypt(session_data, self._key)

        with open(self._session_stored_file, 'w') as f:
            f.write(str(encrypted_session_data))

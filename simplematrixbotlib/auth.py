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
    def __init__(self, homeserver, username, password):
        """
        Initializes the simplematrixbotlib.Creds class.

        Parameters
        ----------
        homeserver : str
            The homeserver for the bot to connect to. Begins with "https://".
    
        username : str
            The username for the bot to connect as.
    
        password : str
            The password for the bot to connect with.

        """

        self.homeserver = homeserver
        self.username = username
        self.password = password

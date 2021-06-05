class Creds:
    """
    A class to store and handle login credentials
    """
    def __init__(self, homeserver, username, password):
        self.homeserver = homeserver
        self.username = username
        self.password = password

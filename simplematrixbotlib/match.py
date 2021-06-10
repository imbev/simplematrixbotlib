class MessageMatch:
    """
    Class with methods to filter messages

    ...
    
    """
    def __init__(self, room, message, bot):
        """
        Initializes the simplematrixbotlib.MessageMatch class.

        ...

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
            The bot developer will use the room parameter of the command function for this.
    
        message : nio.events.room_events.Event
            The bot developer will use the message parameter of the command function for this.
        
        bot : simplematrixbotlib.Bot
            The bot developer will use the bot's instance of the simplematrixbotlib.Bot class for this.

        """

        self.room = room
        self.message = message
        self.bot = bot
        self._prefix = ''
        self._command = ''

    def prefix(self, prefix):
        """
        Parameters
        ----------
        prefix : str
            Beginning of messages that are intended to be commands, usually "!", "/" or similar

        Returns
        -------
        boolean
            Returns True if the message begins with the given arg.
        """
        self._prefix = prefix
        return self.message.body.startswith(prefix)

    def command(self, command):
        """
        Parameters
        ----------
        command : str
            Beginning of messages that are intended to be commands, but after the prefix; e.g. "help".

        Returns
        -------
        boolean
            Returns True if the string following the prefix begins with the given arg. If Match.prefix has not been called, it is assumed that the command does not have a prefix
        """
        self._command = command
        self.args = self.message.body.replace(self._prefix + self._command, '')
        return self.message.body.replace(self._prefix,
                                         '').split(' ')[0] == self._command

    def not_from_this_bot(self):
        """
        Returns
        -------
        boolean
            Returns true if the message was not sent by this bot
        """
        return not self.message.sender == self.bot.async_client.user_id

    def contains(self, string):
        """
        Parameters
        ----------
        string : str
            String to test if it is part of the message.

        Returns
        -------
        boolean
            Returns true if the message contains the given arg
        """
        return string in self.message.body

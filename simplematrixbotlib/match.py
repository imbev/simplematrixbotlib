class Match:
    """
    Class with methods to filter events

    ...

    """
    def __init__(self, room, event, bot) -> None:
        """
        Initializes the simplematrixbotlib.Match class.

        ...

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
            The bot developer will use the room parameter of the handler function for this.
    
        event : nio.events.room_events.Event
            The bot developer will use the event parameter of the handler function for this.
        
        bot : simplematrixbotlib.Bot
            The bot developer will use the bot's instance of the simplematrixbotlib.Bot class for this.

        """
        self.room = room
        self.event = event
        self._bot = bot

    def is_from_userid(self, userid):
        """
        Parameters
        ----------
        userid : str
            The userid of a user.

        Returns
        -------
        boolean
            Returns True if the event was sent from the specified userid
        """
        return self.event.sender == userid

    def is_not_from_this_bot(self):
        """
        
        Returns
        -------
        boolean
            Returns True if the event is from a user that is not this bot.
        """
        return not self.is_from_userid(self._bot.async_client.user_id)


class MessageMatch(Match):
    """
    Class with methods to filter message events

    ...

    """
    def __init__(self, room, event, bot, prefix="") -> None:
        """
        Initializes the simplematrixbotlib.MessageMatch class.

        ...

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
            The bot developer will use the room parameter of the handler function for this.
    
        event : nio.events.room_events.Event
            The bot developer will use the event parameter of the handler function for this.
        
        bot : simplematrixbotlib.Bot
            The bot developer will use the bot's instance of the simplematrixbotlib.Bot class for this.

        prefix : str, Optional
            The bot developer will specify a prefix, the prefix is the beginning of messages that are intended to be commands, usually "!", "/" or similar.

        """
        super().__init__(room, event, bot)
        self._prefix = prefix
        bot_user = self.room.users[self.room.own_user_id]
        self._display_name = bot_user.display_name
        self._disambiguated_name = bot_user.disambiguated_name
        self._pill = f'<a href="https://matrix.to/#/{self.room.own_user_id}">'

    def command(self, command=None):
        """
        Parameters
        ----------
        command : str, Optional
            Beginning of messages that are intended to be commands, but after the prefix; e.g. "help".

        Returns
        -------
        boolean
            Returns True if the string after the prefix and before the first space is the same as the given arg.
        
        str
            Returns the string after the prefix and before the first space if no arg is passed to this method.
        """

        if self._prefix == self.event.body[0:len(self._prefix)]:
            body_without_prefix = self.event.body[len(self._prefix):]
        elif self.mention():
            # the order is important here!
            # note: we assume that body and formatted_body, if present, match as a workaraound of cleaning html
            if self.event.body.startswith(self._disambiguated_name):
                body_without_prefix = self.event.body[len(self._disambiguated_name):]
            elif self.event.body.startswith(self._display_name):
                body_without_prefix = self.event.body[len(self._display_name):]
            elif self.event.body.startswith(self.room.own_user_id):
                body_without_prefix = self.event.body[len(self.room.own_user_id):]
            elif self.event.formatted_body.startswith(self._pill):
                name = self.event.formatted_body[len(self._pill):self.event.formatted_body.index('</a>')]
                body_without_prefix = body_without_prefix = self.event.body[len(name):]
            # mentioning may include a : (colon) as inserted by Element when clicking on a user
            if body_without_prefix.startswith(':'):
                body_without_prefix = body_without_prefix[1:]
        else:
            body_without_prefix = self.event.body

        if not body_without_prefix:
            return []

        if command:
            return body_without_prefix.split()[0] == command
        else:
            return body_without_prefix.split()[0]

    def prefix(self):
        """

        Returns
        -------
        boolean
            Returns True if the message begins with the prefix, and False otherwise. If there is no prefix specified during the creation of this MessageMatch object, then return True.
        """

        return self.event.body.startswith(self._prefix)

    def mention(self):
        """

        Returns
        -------
        boolean
            Returns True if the message begins with the bot's username, MXID, or pill targeting the MXID, and False otherwise.
        """

        for i in [self._display_name, self._disambiguated_name, self.room.own_user_id, self._pill]:
            body = self.event.formatted_body or self.event.body
            if body.startswith(i):
                return True

        return False

    def args(self):
        """
        
        Returns
        -------
        list
            Returns a list of strings that are the "words" of the message, except for the first "word", which would be the command.
        """

        return self.event.body.split()[1:]

    def contains(self, string):
        """
        
        Returns
        -------
        boolean
            Returns True if the string argument is found within the body of the message.
        """

        return string in self.event.body

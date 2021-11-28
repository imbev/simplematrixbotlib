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

        """Forms of identification"""
        self._own_user_id = f"@{self._bot.creds.username}:{self._bot.creds.homeserver.replace("https://","").replace("http://","")}"
        self._own_nio_user = self.room.users[own_user_id]
        self._own_disambiguated_name = own_nio_user.disambiguated_name
        self._own_display_name = own_nio_user.display_name
        self._own_pill = f"<a href=\"https://matrix.to/#/{self.room.own_user_id}\">"

        self.mention() # Set self._mention_id_length
        self._body_without_prefix = self.event.body[len(self._prefix):]
        self._body_without_mention = self.event.body[len(self._mention_id_length):]
        
        if self.mention():
            body = self._body_without_mention
        elif self.prefix():
            body = self._body_without_prefix
        else:
            body = self.event.body
        self._split_body = body.split()

    def command(self, command="") -> Union[bool, str]:
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

        if not (self._body_without_prefix and self._body_without_mention):
            if command:
                return False
            else:
                return ""

        if command:
            return self._split_body[0] == command
        else:
            return self._split_body[0]

    def prefix(self):
        """

        Returns
        -------
        boolean
            Returns True if the message begins with the prefix, and False otherwise. If there is no prefix specified during the creation of this MessageMatch object, then return True.
        """

        return self.event.body[self._mention_id_length:].startswith(self._prefix)

    def mention(self):
        """

        Returns
        -------
        boolean
            Returns True if the message begins with the bot's username, MXID, or pill targeting the MXID, and False otherwise.
        """

        for id in [self._own_disambiguated_name, self._own_display_name, self._own_user_id]:
            if self.event.body.startswith(id):
                self._mention_id_length = len(id)
                return True
                
        return False

    def args(self):
        """
        
        Returns
        -------
        list
            Returns a list of strings that are the "words" of the message, except for the first "word", which would be the prefix/mention + command.
        """

        return self._split_body[1:]

    def contains(self, string):
        """
        
        Returns
        -------
        boolean
            Returns True if the string argument is found within the body of the message.
        """

        return string in self.event.body

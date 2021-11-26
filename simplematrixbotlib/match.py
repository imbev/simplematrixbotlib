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
        self._body_without_prefix = None

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

        # we cache this part
        if self._body_without_prefix is None:
            if self._prefix == self.event.body[0:len(self._prefix)]:
                self._body_without_prefix = self.event.body[len(self._prefix):]
            elif not self.mention():  # if mention() is True then it also sets the _body_without_prefix
                self._body_without_prefix = self.event.body

        if command:
            return self._body_without_prefix.split()[0] == command
        else:
            return self._body_without_prefix.split()[0]

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

        body = self.event.body
        for id in [self._disambiguated_name, self._display_name, self.room.own_user_id]:
            if body.startswith(id):
                body_ = body[len(id):]
                # the match needs to end here, otherwise someone else is mentioned
                # this isn't perfect but probably the best effort
                if body_[0] in [' ', ':']:
                    self._body_without_prefix = body_[1:].strip()
                    return True

        # pills on the other hand are a clearer case thanks to HTML tags which include delimiters
        body = self.event.formatted_body
        if body is not None and body.startswith(self._pill):
            # remove the first half of the pill
            body = body[len(self._pill):]
            # find pill end + trailing delimiter + maybe whitespace
            self._body_without_prefix = body[body.index('</a>')+5:].strip()
            return True

        return False

    def args(self):
        """
        
        Returns
        -------
        list
            Returns a list of strings that are the "words" of the message, except for the first "word", which would be the command.
        """

        return self._body_without_prefix.split()[1:]

    def contains(self, string):
        """
        
        Returns
        -------
        boolean
            Returns True if the string argument is found within the body of the message.
        """

        return string in self.event.body

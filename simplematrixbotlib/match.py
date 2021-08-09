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
            The bot developer will use the room parameter of the command handler for this.
    
        event : nio.events.room_events.Event
            The bot developer will use the event parameter of the command function for this.
        
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
            Returns true if the event was sent from the specified userid
        """
        return self.event.sender == userid

class MessageMatch:
    """
    Class with methods to filter messages
    """
    def __init__(self, room, message, bot):
        self.room = room
        self.message = message
        self.bot = bot
        self._prefix = ''
        self._command = ''

    def prefix(self, prefix):
        """
        Returns True if the message begins with the given arg. Beginning of messages that are intended to be commands, usually "!", "/" or similar
        """
        self._prefix = prefix
        return self.message.body.startswith(prefix)

    def command(self, command):
        """
        Returns True if the string following the prefix begins with the given arg. If Match.prefix has not been called, it is assumed that the command does not have a prefix
        """
        self._command = command
        self.args = self.message.body.replace(self._prefix + self._command, '')
        return self.message.body.replace(self._prefix, '').startswith(command)

    def not_from_this_bot(self):
        """
        Returns true if the message was not sent by this bot
        """
        return not self.message.sender == self.bot.async_client.user_id

    def contains(self, string):
        """
        Returns true if the message contains the given arg
        """
        return string in self.message.body

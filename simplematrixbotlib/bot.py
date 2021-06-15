import asyncio
import simplematrixbotlib as botlib


class Bot:
    """
    A class for the bot library user to interact with.
    
    ...

    Attributes
    ----------
    api : simplematrixbotlib.Api
        An instance of the simplematrixbotlib.Api class.
    
    """
    def __init__(self, creds):
        """
        Initializes the simplematrixbotlib.Bot class.

        Parameters
        ----------
        creds : simplematrixbotlib.Creds

        """

        self.creds = creds
        self.api = botlib.Api(self.creds)
        self.message_actions = []
        self.startup_actions = []

    async def main(self):
        await self.api.login()
        self.async_client = self.api.async_client

        await self.async_client.sync(timeout=65536,
                                     full_state=False)  #Ignore prior messages

        self.callbacks = botlib.Callbacks(self.async_client, self)
        await self.callbacks.setup_callbacks()

        for action in self.startup_actions:
            for room_id in self.async_client.rooms:
                await action(room_id)

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def add_message_listener(self, action_func):
        """
        Adds message callbacks to the message listener.

        Parameteres
        -----------
        
        action_func : function

        """
        self.message_actions.append(action_func)

    def add_startup_action(self, action_func):
        """
        Adds action to be executed at bot start after bot login.

        Parameteres
        -----------
        
        action_func : function

        """
        self.startup_actions.append(action_func)

    def run(self):
        """
        Runs the bot.

        """

        asyncio.get_event_loop().run_until_complete(self.main())

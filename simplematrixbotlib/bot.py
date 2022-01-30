import asyncio
import sys
from typing import Optional
import simplematrixbotlib as botlib
from nio import SyncResponse


class Bot:
    """
    A class for the bot library user to interact with.
    
    ...

    Attributes
    ----------
    api : simplematrixbotlib.Api
        An instance of the simplematrixbotlib.Api class.
    
    """

    def __init__(self, creds, config=None):
        """
        Initializes the simplematrixbotlib.Bot class.

        Parameters
        ----------
        creds : simplematrixbotlib.Creds

        """

        self.creds = creds
        self.api = botlib.Api(self.creds)
        if config:
            self.config = config
            self._need_allow_homeserver_users = False
        else:
            self._need_allow_homeserver_users = True
            self.config = botlib.Config()
        self.listener = botlib.Listener(self)

    async def main(self):

        self.creds.session_read_file()

        if not (await self.api.check_valid_homeserver(self.creds.homeserver)):
            raise ValueError("Invalid Homeserver")

        await self.api.login()

        self.async_client = self.api.async_client

        resp = await self.async_client.sync(timeout=65536, full_state=False
                                            )  #Ignore prior messages

        if isinstance(resp, SyncResponse):
            print(
                f"Connected to {self.async_client.homeserver} as {self.async_client.user_id} ({self.async_client.device_id})"
            )

        self.creds.session_write_file()

        if self._need_allow_homeserver_users:
            # allow (only) users from our own homeserver by default
            hs: str = self.api.async_client.user_id[self.api.async_client.
                                                    user_id.index(":") +
                                                    1:].replace('.', '\\.')
            self.config.allowlist = set([f"(.+):{hs}"])

        self.callbacks = botlib.Callbacks(self.async_client, self)
        await self.callbacks.setup_callbacks()

        for action in self.listener._startup_registry:
            for room_id in self.async_client.rooms:
                await action(room_id)

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def run(self):
        """
        Runs the bot.

        """

        asyncio.run(self.main())

import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)

class Api:
    """
    A class to interact with the matrix-nio library.
    """
    def __init__(self, creds):
        self.creds = creds

    def login(self):
        """
        Login the client to the homeserver
        """
        self.client = AsyncClient(
            self.creds.homeserver,
            self.creds.username
        )
        response = await async_client.login(creds.password)
        print(response)

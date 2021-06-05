import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)


class API:
    """
    A class to interact with the matrix-nio library.
    """
    def __init__(self, creds):
        self.creds = creds

    async def login(self):
        """
        Login the client to the homeserver
        """
        self.async_client = AsyncClient(self.creds.homeserver,
                                        self.creds.username)

        response = await self.async_client.login(self.creds.password)
        print(response)

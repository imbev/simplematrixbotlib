import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)


class Api:
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

    async def send_text_message(self, room_id, message):
        await self.async_client.room_send(room_id=room_id,
                                          message_type="m.room.message",
                                          content={
                                              "msgtype": "m.text",
                                              "body": message
                                          })

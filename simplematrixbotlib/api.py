import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)


class Api:
    """
    A class to interact with the matrix-nio library. Usually used by the Bot class, and sparingly by the bot developer.

    ...

    Attributes
    ----------
    creds : simplematrixbotlib.Creds

    """
    def __init__(self, creds):
        """
        Initializes the simplematrixbotlib.Api class.

        Parameters
        ----------
        creds : simplematrixbotlib.Creds

        """
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
        """
        Send a text message in a Matrix room.

        Parameteres
        -----------
        room_id : str
            The room id of the destination of the message.
        
        message : str
            The content of the message to be sent.

        """
        await self.async_client.room_send(room_id=room_id,
                                          message_type="m.room.message",
                                          content={
                                              "msgtype": "m.text",
                                              "body": message
                                          })

import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)
from PIL import Image
import aiofiles.os
import mimetypes
import os
import markdown

from nio.responses import UploadResponse


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

        self.creds.session_read_file()

        self.async_client = AsyncClient(self.creds.homeserver,
                                        self.creds.username)

        if self.creds.device_id:
            self.async_client.device_id = self.creds.device_id

        if self.creds.password or self.creds.login_token:
            response = await self.async_client.login(
                password=self.creds.password,
                device_name='Bot Client built with Simple-Matrix-Bot-Lib',
                token=self.creds.login_token)
            print(response)

            self.creds.device_id = response.device_id
            self.creds.access_token = response.access_token

        else:
            self.async_client.access_token = self.creds.access_token
            self.async_client.user_id = f"@{self.creds.username}:{self.creds.homeserver}"
            self.async_client.device_id = self.creds.device_id

        self.creds.session_write_file()

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

    async def send_image_message(self, room_id, image_filepath):
        """
        Send an image message in a Matrix room.

        Parameteres
        -----------
        room_id : str
            The room id of the destination of the message.

        image_filepath : str
            The path to the image on your machien.
        """

        mime_type = mimetypes.guess_type(image_filepath)[0]

        image = Image.open(image_filepath)
        (width, height) = image.size

        file_stat = await aiofiles.os.stat(image_filepath)
        async with aiofiles.open(image_filepath, "r+b") as file:
            resp, maybe_keys = await self.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(image_filepath),
                filesize=file_stat.st_size)
        if isinstance(resp, UploadResponse):
            pass  #Successful upload
        else:
            print(f"Failed Upload Response: {resp}")

        content = {
            "body": os.path.basename(image_filepath),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": None,
                "w": width,
                "h": height,
                "thumbnail_url": None
            },
            "msgtype": "m.image",
            "url": resp.content_uri
        }

        try:
            await self.async_client.room_send(room_id,
                                              message_type="m.room.message",
                                              content=content)
        except:
            print(f"Failed to send image file {image_filepath}")

    async def send_markdown_message(self, room_id, message):
        """
        Send a markdown message in a Matrix room.

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
                                              "msgtype":
                                              "m.text",
                                              "body":
                                              message,
                                              "format":
                                              "org.matrix.custom.html",
                                              "formatted_body":
                                              markdown.markdown(message)
                                          })

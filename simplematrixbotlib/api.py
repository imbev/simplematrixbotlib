import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText, RoomMessageFormatted)
from PIL import Image
import aiofiles.os
import mimetypes
import os
import markdown as md
import aiohttp
import ast
from nio.responses import UploadResponse
import nio


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

        if not self.creds.homeserver:
            raise ValueError("Missing homeserver")
        if not self.creds.username:
            raise ValueError("Missing Username")
        if not (self.creds.password or self.creds.login_token or self.creds.access_token):
            raise ValueError("Missing password, login token, access token. Either password, login token or access token must be provided")

        self.async_client = AsyncClient(homeserver=self.creds.homeserver, user=self.creds.username, device_id=self.creds.device_id)

        if self.creds.password:
            resp = await self.async_client.login(password=self.creds.password,  device_name=self.creds.device_name)

        elif self.creds.access_token:
            self.async_client.access_token = self.creds.access_token

            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.creds.homeserver}/_matrix/client/r0/account/whoami?access_token={self.creds.access_token}') as response:
                    device_id = ast.literal_eval((await response.text()).replace(":false,", ":\"false\","))['device_id']
                    user_id = ast.literal_eval((await response.text()).replace(":false,", ":\"false\","))['user_id']
            
            self.async_client.device_id, self.creds.device_id = device_id, device_id
            self.async_client.user_id, self.creds.user_id = user_id, user_id
            resp = None

        elif self.creds.login_token:
            resp = await self.async_client.login(token=self.creds.login_token,  device_name=self.creds.device_name)
        
        if isinstance(resp, nio.responses.LoginError):
            raise Exception(resp)
    
    async def check_valid_homeserver(self, homeserver: str) -> bool:
        if not (homeserver.startswith('http://') or homeserver.startswith('https://')):
            return False
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f'{homeserver}/_matrix/client/versions') as response:
                    if response.status == 200:
                        return True
            except aiohttp.client_exceptions.ClientConnectorError:
                return False
        
        return False

    async def send_text_message(self, room_id, message, msgtype='m.text', reply_to=None, markdown=False):
        """
        Send a text message in a Matrix room.

        Parameters
        -----------
        room_id : str
            The room id of the destination of the message.

        message : str
            The content of the message to be sent.

        msgtype : str, optional
            The type of message to send: m.text (default), m.notice, etc

        reply_to : nio.events.room_events.RoomMessage, optional
            The event to reply to

        markdown : Boolean, optional
            Whether to treat message as markdown and render as HTML

        """
        content = {
                      "msgtype": msgtype,
                      "body": message
                  }

        if markdown or reply_to is not None:
            content["format"] = "org.matrix.custom.html"
            content["formatted_body"] = md.markdown(message, extensions=['nl2br'])

        if reply_to is not None:
            content["m.relates.to"] = {"m.in_reply_to": {"event_id": reply_to.event_id}}
            if isinstance(reply_to, RoomMessageFormatted):  # quote fallback if it's a text event https://spec.matrix.org/unstable/client-server-api/#fallbacks-for-rich-replies
                content["body"] = f'> <{reply_to.sender}> {reply_to.body}\n\n{content["body"]}'
                formatted_body = f'<mx-reply><blockquote><a href="https://matrix.to/#/{room_id}/{reply_to.event_id}">In reply to</a> '
                formatted_body += f'<a href="https://matrix.to/#/{reply_to.sender}">{reply_to.sender}</a><br>'
                formatted_body += f'{reply_to.formatted_body or reply_to.body}</blockquote></mx-reply>{content["formatted_body"]}'
                content["formatted_body"] = formatted_body

        await self.async_client.room_send(room_id=room_id,
                                          message_type="m.room.message",
                                          content=content,
                                          ignore_unverified_devices=True)

    async def send_markdown_message(self, room_id, message, msgtype='m.text', reply_to=None):
        """
        Send a markdown message in a Matrix room.
        Wrapper for send_text_message

        Parameters
        -----------
        room_id : str
            The room id of the destination of the message.

        message : str
            The content of the message to be sent.

        msgtype : str, optional
            The type of message to send: m.text (default), m.notice, etc

        reply_to : nio.events.room_events.RoomMessage, optional
            The event to reply to

        """
        await self.send_text_message(room_id=room_id, message=message, msgtype=msgtype, reply_to=reply_to, markdown=True)

    async def send_image_message(self, room_id, image_filepath):
        """
        Send an image message in a Matrix room.

        Parameters
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
                                              content=content,
                                              ignore_unverified_devices=True)
        except:
            print(f"Failed to send image file {image_filepath}")

import json
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText, AsyncClientConfig)
from nio.exceptions import OlmUnverifiedDeviceError
from nio.responses import UploadResponse
import nio
from PIL import Image
import aiofiles.os
import mimetypes
import os
import markdown
import aiohttp
from typing import List, Tuple, Union
import re


async def check_valid_homeserver(homeserver: str) -> bool:
    if not (homeserver.startswith('http://')
            or homeserver.startswith('https://')):
        return False

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    f'{homeserver}/_matrix/client/versions') as response:
                if response.status == 200:
                    return True
        except aiohttp.client_exceptions.ClientConnectorError:
            return False

    return False


def split_mxid(mxid: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    # s = mxid.split(':')
    # if len(s) != 2 or s[0][0] != '@':
    #     return None, None
    # s[0] = s[0][1:]
    match = re.match(
        r'@(?P<localpart>[^:]*):(?P<hostname>(?P<ipv4>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?P<ipv6>\[[\da-fA-F:.]{2,45}\])|(?P<dns>[a-zA-Z\d\-.]{1,255}))(?P<port>:\d{1,5})?',
        mxid)
    if match is None:
        return None, None
    return match.group('localpart'), match.group('hostname')


class Api:
    """
    A class to interact with the matrix-nio library. Usually used by the Bot class, and sparingly by the bot developer.

    ...

    Attributes
    ----------
    creds : simplematrixbotlib.Creds

    """

    def __init__(self, creds, config):
        """
        Initializes the simplematrixbotlib.Api class.

        Parameters
        ----------
        creds : simplematrixbotlib.Creds

        """
        self.creds = creds
        self.config = config
        self.async_client: AsyncClient = None

    async def login(self):
        """
        Login the client to the homeserver

        """

        if not self.creds.homeserver:
            raise ValueError("Missing homeserver")
        if not self.creds.username:
            raise ValueError("Missing Username")
        if not (self.creds.password or self.creds.login_token
                or self.creds.access_token):
            raise ValueError(
                "Missing password, login token, access token. Either password, login token or access token must be provided"
            )

        client_config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            store_sync_tokens=True,
            encryption_enabled=self.config.encryption_enabled)
        store_path = self.config.store_path
        os.makedirs(store_path, mode=0o750, exist_ok=True)
        self.async_client = AsyncClient(homeserver=self.creds.homeserver,
                                        user=self.creds.username,
                                        device_id=self.creds.device_id,
                                        store_path=store_path,
                                        config=client_config)

        if self.creds.access_token:
            self.async_client.access_token = self.creds.access_token

            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'{self.creds.homeserver}/_matrix/client/r0/account/whoami?access_token={self.creds.access_token}'
                ) as response:
                    if isinstance(response, nio.responses.LoginError):
                        raise Exception(response)

                    r = json.loads(
                        (await
                         response.text()).replace(":false,", ":\"false\","))
                    device_id = r['device_id']
                    self.async_client.user_id, user_id = (r['user_id'],
                                                          r['user_id'])

            if self.creds.username == split_mxid(user_id)[0]:
                # save full MXID
                self.creds.username = user_id
            elif user_id != self.creds.username:
                raise ValueError(
                    f"Given Matrix ID (username) '{user_id}' does not match the access token. "
                    "This error prevents you from accidentally using the wrong account. "
                    "Resolve this by providing the correct username with your credentials, "
                    f"or reset your session by deleting {self.creds._session_stored_file}"
                    f"{' and ' + self.config.store_path if self.config.encryption_enabled else ''}."
                )
            if device_id != self.creds.device_id:
                if self.config.encryption_enabled:
                    if self.creds.device_id is not None:
                        raise ValueError(
                            f"Given device ID (session ID) '{device_id}' does not match the access token. "
                            "This is critical, because it may break your verification status unintentionally. "
                            "Fix this by providing the correct credentials matching the stored session "
                            f"{self.creds._session_stored_file}.")
                    else:
                        print(
                            "First run with access token. "
                            "Saving device ID (session ID)...")
                        self.creds.device_id, self.async_client.device_id = (device_id, device_id)
                        self.creds.session_write_file()
                else:
                    print(
                        "Loaded device ID (session ID) does not match the access token. "
                        "Recovering automatically...")
                    self.creds.device_id, self.async_client.device_id = (device_id, device_id)
                    self.creds.session_write_file()

            if self.config.encryption_enabled:
                self.async_client.load_store()

        else:
            if self.creds.password:
                resp = await self.async_client.login(
                    password=self.creds.password,
                    device_name=self.creds.device_name)

            elif self.creds.login_token:
                resp = await self.async_client.login(
                    token=self.creds.login_token,
                    device_name=self.creds.device_name)

            else:
                raise ValueError(
                    "Can't log in: Missing access token, password, or login token"
                )

            if isinstance(resp, nio.responses.LoginError):
                raise Exception(resp)

            self.creds.device_id = resp.device_id
            self.creds.access_token = resp.access_token

        if self.async_client.should_upload_keys:
            await self.async_client.keys_upload()

    async def _send_room(self,
                         room_id,
                         content,
                         message_type="m.room.message",
                         ignore_unverified_devices=None):
        try:
            await self.async_client.room_send(
                room_id=room_id,
                message_type=message_type,
                content=content,
                ignore_unverified_devices=ignore_unverified_devices
                                          or self.config.ignore_unverified_devices)
        except OlmUnverifiedDeviceError as e:
            # print(str(e))
            print(
                "Message could not be sent. "
                "Set ignore_unverified_devices = True to allow sending to unverified devices."
            )
            print("Automatically blacklisting the following devices:")
            for user in self.async_client.rooms[room_id].users:
                unverified: List[str] = list()
                for device_id, device in self.async_client.olm.device_store[
                    user].items():
                    if not (self.async_client.olm.is_device_verified(device) or
                            self.async_client.olm.is_device_blacklisted(device)
                    ):
                        self.async_client.olm.blacklist_device(device)
                        unverified.append(device_id)
                if len(unverified) > 0:
                    print(f"\tUser {user}: {', '.join(unverified)}")

            await self.async_client.room_send(
                room_id=room_id,
                message_type=message_type,
                content=content,
                ignore_unverified_devices=ignore_unverified_devices
                                          or self.config.ignore_unverified_devices)

    async def send_text_message(self, room_id, message, msgtype='m.text'):
        """
        Send a text message in a Matrix room.

        Parameteres
        -----------
        room_id : str
            The room id of the destination of the message.

        message : str
            The content of the message to be sent.

        msgtype : str, optional
            The type of message to send: m.text (default), m.notice, etc

        """
        await self._send_room(room_id=room_id,
                              content={
                                  "msgtype": msgtype,
                                  "body": message
                              })

    async def send_markdown_message(self, room_id, message, msgtype='m.text'):
        """
        Send a markdown message in a Matrix room.

        Parameteres
        -----------
        room_id : str
            The room id of the destination of the message.

        message : str
            The content of the message to be sent.

        msgtype : str, optional
            The type of message to send: m.text (default), m.notice, etc

        """

        await self._send_room(room_id=room_id,
                              content={
                                  "msgtype":
                                      msgtype,
                                  "body":
                                      message,
                                  "format":
                                      "org.matrix.custom.html",
                                  "formatted_body":
                                      markdown.markdown(message,
                                                        extensions=['nl2br'])
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
            pass  # Successful upload
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
            await self._send_room(room_id=room_id, content=content)
        except:
            print(f"Failed to send image file {image_filepath}")

    async def send_video_message(self, room_id, video_filepath):
        """
        Send a video message in a Matrix room.

        Parameters
        ----------
        room_id : str
            The room id of the destination of the message.

        video_filepath : str
            The path to the video on your machine.
        """

        mime_type = mimetypes.guess_type(video_filepath)[0]

        file_stat = await aiofiles.os.stat(video_filepath)
        async with aiofiles.open(video_filepath, "r+b") as file:
            resp, maybe_keys = await self.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(video_filepath),
                filesize=file_stat.st_size)

        if isinstance(resp, UploadResponse):
            pass # Successful upload
        else:
            print(f"Failed Upload Response: {resp}")

        content = {
            "body": os.path.basename(video_filepath),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": None
            },
            "msgtype": "m.video",
            "url": resp.content_uri
        }
        
        try:
            await self._send_room(room_id=room_id, content=content)
        except:
            print(f"Failed to send video file {video_filepath}")


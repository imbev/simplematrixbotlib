from nio import InviteMemberEvent, RoomMessageText
from nio import MegolmEvent


class Callbacks:
    """
    A class for handling callbacks.

    ...

    """

    def __init__(self, async_client, bot):
        self.async_client = async_client
        self.bot = bot

    async def setup_callbacks(self):
        """
        Add callbacks to async_client

        """
        if self.bot.config.join_on_invite:
            self.async_client.add_event_callback(self.invite_callback,
                                                 InviteMemberEvent)

        self.async_client.add_event_callback(self.decryption_failure,
                                             MegolmEvent)

        for event_listener in self.bot.listener._registry:
            self.async_client.add_event_callback(event_listener[0],
                                                 event_listener[1])

    async def invite_callback(self, room, event, tries=1):
        """
        Callback for handling invites.

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
        event : nio.events.room_events.InviteMemberEvent
        tries : int, optional
            Amount of times that this function has been called in a row for the same exact event.

        """
        if not event.membership == "invite":
            return

        try:
            await self.async_client.join(room.room_id)
            print(f"Joined {room.room_id}")
        except Exception as e:
            print(f"Error joining {room.room_id}: {e}")
            tries += 1
            if not tries == 3:
                print("Trying again...")
                await self.invite_callback(room, event, tries)
            else:
                print(f"Failed to join {room.room_id} after 3 tries")

    async def decryption_failure(self, room, event):
        """
        Callback for handling decryption errors.

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
        event : nio.events.room_events.MegolmEvent

        """
        if not isinstance(event, MegolmEvent):
            return

        print(f"failed to decrypt message: {event.event_id} from {event.sender}")
        await bot.api.send_text_message(room.room_id, "Failed to decrypt your message. Make sure you are sending messages to unverified devices or verify me if possible.", msgtype='m.notice')

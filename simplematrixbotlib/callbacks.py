from nio import InviteMemberEvent, RoomMessageText


class Callbacks:
    def __init__(self, async_client, bot):
        self.async_client = async_client
        self.bot = bot

    async def setup_callbacks(self):
        """
        Add callbacks to async_client
        """
        self.async_client.add_event_callback(self.invite_callback,
                                             InviteMemberEvent)
        self.async_client.add_event_callback(self.message_callback,
                                             RoomMessageText)

    async def invite_callback(self, room, event, tries=1):
        """
        callback for handling invites
        """
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

    async def message_callback(self, room, event):
        """
        callback for handling messages
        """
        for action in self.bot.message_actions:
            await action(room, event)

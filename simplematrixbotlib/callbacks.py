from nio import InviteMemberEvent


class Callbacks:
    def __init__(self, async_client):
        self.async_client = async_client

    async def setup_callbacks(self):
        """
        Add callbacks to async_client
        """
        self.async_client.add_event_callback(self.invite_callback,
                                             InviteMemberEvent)

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

import nio.events.room_events
import nio.events.to_device
from nio import InviteMemberEvent
from nio import MegolmEvent, KeyVerificationStart, KeyVerificationCancel, KeyVerificationKey, KeyVerificationMac, ToDeviceError, KeyVerificationEvent


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

        if self.bot.config.emoji_verify:
            self.async_client.add_to_device_callback(self.emoji_verification,
                                                     (KeyVerificationEvent, ))

        for event_listener in self.bot.listener._registry:
            if issubclass(event_listener[1],
                          nio.events.to_device.ToDeviceEvent):
                self.async_client.add_to_device_callback(
                    event_listener[0], event_listener[1])
            else:
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

        print(
            f"Failed to decrypt message: {event.event_id} from {event.sender} in {room.room_id}. "
            "If this error persists despite verification, reset the crypto session by deleting "
            f"{self.bot.config.store_path} and {self.bot.creds._session_stored_file}. "
            "You will have to verify any verified devices anew.")
        await self.bot.api.send_text_message(
            room.room_id, "Failed to decrypt your message. "
            "Make sure encryption is enabled in my config and "
            "either enable sending messages to unverified devices or verify me if possible.",
            msgtype='m.notice')

    async def emoji_verification(self, event):
        """
        Callback for handling interactive verification using emoji.
        Copied from
        https://github.com/poljar/matrix-nio/blob/8ac48ed0fda5da129c008e129305a512e8619cde/examples/verify_with_emoji.py
        with explanation comments removed and miniscule changes

        Parameters
        ----------
        event : nio.events.to_device.KeyVerificationEvent

        """
        try:
            if isinstance(event, KeyVerificationStart
                          ):  # first step: receive m.key.verification.start
                if "emoji" not in event.short_authentication_string:
                    print("Other device does not support emoji verification "
                          f"{event.short_authentication_string}.")
                    return
                # send m.key.verification.accept
                resp = await self.async_client.accept_key_verification(
                    event.transaction_id)
                if isinstance(resp, ToDeviceError):
                    print(f"accept_key_verification failed with {resp}")

                sas = self.async_client.key_verifications[event.transaction_id]

                # send m.key.verification.key
                todevice_msg = sas.share_key()
                resp = await self.async_client.to_device(todevice_msg)
                if isinstance(resp, ToDeviceError):
                    print(f"to_device failed with {resp}")

            elif isinstance(event, KeyVerificationCancel):  # anytime
                # There is no need to issue a
                # self.async_client.cancel_key_verification(tx_id, reject=False)
                # here. The SAS flow is already cancelled.
                # We only need to inform the user.
                print(f"Verification has been cancelled by {event.sender} "
                      f"for reason \"{event.reason}\".")

            elif isinstance(event, KeyVerificationKey
                            ):  # second step: receive m.key.verification.key
                sas = self.async_client.key_verifications[event.transaction_id]

                print(f"{sas.get_emoji()}")

                yn = input("Do the emojis match? (Y/N) (C for Cancel) ")
                if yn.lower() == "y":
                    print("Match! The verification for this "
                          "device will be accepted.")
                    # send m.key.verification.mac
                    resp = await self.async_client.confirm_short_auth_string(
                        event.transaction_id)
                    if isinstance(resp, ToDeviceError):
                        print(f"confirm_short_auth_string failed with {resp}")
                elif yn.lower() == "n":  # no, don't match, reject
                    print("No match! Device will NOT be verified "
                          "by rejecting verification.")
                    resp = await self.async_client.cancel_key_verification(
                        event.transaction_id, reject=True)
                    if isinstance(resp, ToDeviceError):
                        print(f"cancel_key_verification failed with {resp}")
                else:  # C or anything for cancel
                    print("Cancelled by user! Verification will be "
                          "cancelled.")
                    resp = await self.async_client.cancel_key_verification(
                        event.transaction_id, reject=False)
                    if isinstance(resp, ToDeviceError):
                        print(f"cancel_key_verification failed with {resp}")

            elif isinstance(event, KeyVerificationMac
                            ):  # third step: receive m.key.verification.mac
                sas = self.async_client.key_verifications[event.transaction_id]
                try:
                    todevice_msg = sas.get_mac()
                except LocalProtocolError as e:
                    # e.g. it might have been cancelled by ourselves
                    print(f"Cancelled or protocol error: Reason: {e}.\n"
                          f"Verification with {event.sender} not concluded. "
                          "Try again?")
                else:
                    # send m.key.verification.mac
                    resp = await self.async_client.to_device(todevice_msg)
                    if isinstance(resp, ToDeviceError):
                        print(f"to_device failed with {resp}")
                    print(f"sas.we_started_it = {sas.we_started_it}\n"
                          f"sas.sas_accepted = {sas.sas_accepted}\n"
                          f"sas.canceled = {sas.canceled}\n"
                          f"sas.timed_out = {sas.timed_out}\n"
                          f"sas.verified = {sas.verified}\n"
                          f"sas.verified_devices = {sas.verified_devices}\n")
                    print("Emoji verification was successful!")
                    # TODO: share room keys(?) to formerly blacklisted devices
                    # Error: ** Unable to decrypt: decryption key withheld **
            else:
                print(f"Received unexpected event type {type(event)}. "
                      f"Event is {event}. Event will be ignored.")

        except BaseException:
            import traceback
            print(traceback.format_exc())

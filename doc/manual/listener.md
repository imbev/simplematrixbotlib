### How to use the Listener class
The Listener class is a class that is used to specify reactions to the events that occur in Matrix rooms. The source is located at simplematrixbotlib/listener.py

### Accessing a Listener instance
An instance of the Listener class is automatically created when an instance of the Bot class is created. An example is shown in the following python code.
```python
bot = botlib.Bot(creds)
bot.listener #Instance of the Listener class
```

### Using the on_message_event decorator
The on_message_event method of the Listener class may be used to execute actions based on messages that are sent in rooms that the bot is a member of. Example usage of on_message_event is shown in the following python code.
```python
@bot.listener.on_message_event
async def example(room, message):
    print(f"A message({message.content}) was sent in a room({room.room_id}).")

```
When any message is sent, the function will be called with room as a [Room object](https://matrix-nio.readthedocs.io/en/latest/nio.html#nio.rooms.MatrixRoom) representing each room that that the bot is a member of, and message as a [RoomMessage object](https://matrix-nio.readthedocs.io/en/latest/nio.html?highlight=nio.events.room_events.roommessage.content#nio.events.room_events.RoomMessage) representing the message that was sent.

### Using the on_reaction_event decorator
The on_reaction_event decorator method of the Listener class may be used to execute actions based on reactions that are sent in rooms that the bot is a member of. Example usage of on_reaction_event is shown in the following python code.
```python
@bot.listener.on_reaction_event
async def example(room, event, reaction):
    print(f"User {event.source['sender']} reacted with {reaction} to message {event.source['content']['m.relates_to']['event_id']}")
```

As of the time of writing, m.reaction events are not supported via matrix-nio. To work around this, it is recommended to use the event's source via event.source as a dictionary. An example m.reaction event source is provided for convenience below:
```json
{
	"events": [
		{
			"content": {
				"m.relates_to": {
					"event_id": "$FNP1EnwKRuzH38LjuYptDSkJpzomVt3tijlBy6yfc10",
					"key": "😆",
					"rel_type": "m.annotation"
				}
			},
			"origin_server_ts": 1641348447462,
			"sender": "@krazykirby99999:matrix.org",
			"type": "m.reaction",
			"unsigned": {
				"age": 341
			},
			"event_id": "$rGchfmQQmt2NxnlJ88HzWdVTIW-cfo-DGZFUYbqihBI"
		}
	]
}
```

### Using the on_custom_event decorator
The on_custom_event method of the Listener class may be used to execute actions based on any event that is sent in rooms that the bot is a member of. Example usage of on_custom_event is shown in the following python code.
```python
import nio

@bot.listener.on_custom_event(nio.InviteMemberEvent)
async def example(room, event):
    if event.membership == "join":
        print(f"A user joined the room({room.room_id}).")
    if event.membership == "leave":
        print(f"A user left the room({room.room_id}).")

```
The on_custom_event method is almost identical to the on_message_event method. on_custom_event takes an argument that allows the developer to specify the event type for the Bot to respond to. Information on events can be found in the [matrix-nio docs](https://matrix-nio.readthedocs.io/en/latest/nio.html#module-nio.events).

#### Using the on_startup decorator
The on_startup method of the Listener class may be used to execute actions upon the starting of the Bot. Example usage of the on_startup method is show in the following python code.
```python
@bot.listener.on_startup
async def room_joined(room_id):
    print(f"This account is a member of a room with the id {room_id}")
```
When the bot is run, for each room that the Bot is a member of, the function will be called with room_id as a string that corresponds to the room_id of the room.
### How to use the Listener class
The Listener class is a class that is used to specify reactions to the events that occur in Matrix rooms. The source is located at simplematrixbotlib/listener.py

### Accessing a Listener instance
An instance of the Listener class is automatically created when an instance of the Bot class is created. An example is shown in the following python code.
```python
bot = botlib.Bot(creds)
bot.listener #Instance of the Listener class
```

### Using the on_message_event decorator
The on_message_event method of the Bot class may be used to execute actions based on messages that are sent in rooms that the bot is a member of. Example usage of on_message_event is shown in the following python code.
```python
@bot.listener.on_message_event
async def example(room, message):
    print(f"A message({message.content}) was sent in a room({room.room_id}).")

```
When any message is sent, the function will be called with room as a [Room object](https://matrix-nio.readthedocs.io/en/latest/nio.html#nio.rooms.MatrixRoom) representing each room that that the bot is a member of, and message as a [RoomMessage object](https://matrix-nio.readthedocs.io/en/latest/nio.html?highlight=nio.events.room_events.roommessage.content#nio.events.room_events.RoomMessage) representing the message that was sent.



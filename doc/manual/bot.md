### How to use the Bot class
The Bot class is a class that handles most of the functionality of a bot created with Simple-Matrix-Bot-Lib. The source is located at simplematrixbotlib/bot.py.

#### Creating an instance of the Bot class
An instance can be created using the following python code.
```
bot = botlib.Bot(
    creds=creds
    )
```
The creds argument is neccesary, and is an instance of the Creds class.

#### Using the add_message_listener method
The add_message_listener method of the Bot class may be used to execute actions based on messages that are sent in rooms that the bot is a member of. Example usage of add_message_listener is shown in the following python code.
```
async def example(room, message):
    print(f"A message({message.content}) was sent in a room({room.room_id}).")
bot.add_message_listener(example)
```
When any message is sent, the function will be called with room as a [Room object](https://matrix-nio.readthedocs.io/en/latest/nio.html#nio.rooms.MatrixRoom) representing each room that that the bot is a member of, and message as a [RoomMessage object](https://matrix-nio.readthedocs.io/en/latest/nio.html?highlight=nio.events.room_events.roommessage.content#nio.events.room_events.RoomMessage) representing the message that was sent.

#### Using the add_startup_action method
The add_startup_action method of the Bot class may be used to execute actions upon the starting of the Bot. Example usage of the add_startup_action method is show in the following python code.
```
async def room_joined(room_id):
    print(f"This account is a member of a room with the id {room_id}")
bot.add_startup_listener(room_joined)
```
When the bot is run, for each room that the Bot is a member of, the function will be called with room_id as a string that corresponds to the room_id of the room.

#### Running the Bot
When the Bot is ready to be started, the run method can be used to run the Bot. An example is shown in the following python code.
```
bot.run()
```
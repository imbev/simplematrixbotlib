### How to use the Match class

The Match class is a class that handles matching/filtering of the content of events. The source is located at simplematrixbotlib/match.py

#### Creating an instance of the Match class

An instance can be created using the following python code.

```python
match = botlib.Match(
    room=room,
    event=event,
    bot=bot
)
```

The room, event, and bot arguments are neccesary. The room and event arguments should be the same as the arguments of the handler function. The bot argument should be the same as the instance of the Bot class. This class is intended to be used with non-message events, as the MessageMatch class is a child class of this class, and has message-specific methods. A list of methods for the Match class is shown below.

#### <div id="match-methods">List of Methods:</div>

| Method                          | Explanation                                                     |
| ------------------------------- | --------------------------------------------------------------- |
| `Match.is_from_user_id(userid)` | Returns True if the userid argument matches the event's sender. |
| `Match.is_not_from_this_bot()`  | Returns True if the event is not sent by this bot.              |

Example:

```python
bot.listener.on_message_event
async def example(room, event):
    match = botlib.Match(room, event, bot)
    if match.is_not_from_this_bot():
        print(f"A user sent a message in room {room.room_id}")
```

### How to use the MessageMatch class

The MessageMatch class is a class that handles matching/filtering of message events. It is a subclass of the Match class, and thus methods of the Match class can also be used with the MessageMatch class. The source is located at simplematrixbotlib/match.py

#### Creating an instance of the MessageMatch class

An instance can be created using the following python code.

```python
match = botlib.MessageMatch(
    room=room,
    event=event,
    bot=bot,
    prefix="/"
)
```

The room, event, and bot arguments are necessary. The bot argument is an instance of the Bot class. The room and event arguments are the same as the arguments specified when creating a handler function to be used with the Listener.on_message_event method. The prefix argument is usually used as the beginning of messages that are intended to be commands, usually "!", "/" or another short string. An example handler function that uses MessageMatch is shown in the following python code.

```python
bot.listener.on_message_event
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot, "!")
    if match.command("help") and match.prefix(): # Matches any message that begins with "!help "
        #Respond to help command
```

As said earlier, the prefix argument is optional. An example handler function without it is shown in the following python code.

```python
bot.listener.on_message_event
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if match.command("help"): # Matches any message that begins with "help "
        #Respond to help command
```

It is also possible to match by mention of the bot's username, matrix ID, etc.
In the next example, we can use the prefix or mention the bot to show its help message.

```python
bot.listener.on_message_event
async def help(room, message):
    match = botlib.MessageMatch(room, message, bot, "!")
    if match.command("help") and (match.prefix() or match.mention()):
        #Respond to help command
```

A list of methods for the Match class is shown below. [Methods from the Match class](#match-methods) can also be used with the MessageMatch class.

#### List of Methods:

| Method                                                      | Explanation                                                                                                                                                                                                                              |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `MessageMatch.command()` or `MessageMatch.command(command)` | The "command" is the beginning of messages that are intended to be commands, but after the prefix; e.g. "help". Returns the command if the command argument is empty. Returns True if the command argument is equivalent to the command. |
| `MessageMatch.prefix()`                                     | Returns True if the message begins with the prefix specified during the initialization of the instance of the MessageMatch class. Returns True if no prefix was specified during the initialization.                                     |
| `MessageMatch.mention()`                                    | Returns True if the message begins with the bot's display name, disambiguated display name, matrix ID, or pill (HTML link to the bot via matrix.to) if formatted_body is present.                                                        |
| `MessageMatch.args()`                                       | Returns a list of strings; each string is part of the message separated by a space, with the exception of the part of the message before the first space (the prefix and command). Returns an empty list if it is a single-word command. |
| `MessageMatch.contains(string)`                             | Returns True if the message contains the value specified in the string argument.                                                                                                                                                         |

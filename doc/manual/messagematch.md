### How to use the MessageMatch class
The MessageMatch class is a class that handles matching/filtering of the content of message events. The source is located at simplematrixbotlib/match.py

#### Creating an instance of the MessageMatch class
An instance can be created using the following python code.
```python
match = botlib.MessageMatch(
    room=room,
    message=message,
    bot=bot
)
```
All of the arguments are neccesary. The bot argument is an instance of the Bot class. The room and message arguments are the same as the arguments specified when creating a function to be used with the Bot.add_message_listener method. An example of the two combined is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
bot.add_message_listener(example)
```

#### Using the prefix method
The prefix method of the MessageMatch class can be used to filter by messages that begin with a specified prefix. Example usage of the MessageMatch.prefix method is shown in the following python code.
```python
PREFIX = '!'
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if match.prefix(PREFIX):
        #Do Something
bot.add_message_listener(example)
```
In this case, match.prefix(PREFIX) returns True if the message begins with the same value as the PREFIX variable.

#### Using the command method
The command method of the MessageMatch class can be used to filter messages by the string that immediately follows the prefix of the message. The command method returns True if the string following the prefix begins with the command string. The args attribute of the MessageMatch object is set to a string that contains the original message, but with the command ommitted. It will also ommit the prefix if the prefix method was called before this method. An example is shown in the following python code.
```python
PREFIX = '!'
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    COMMAND = "example"
    if (match.prefix(PREFIX) and #Returns True if the message begins with PREFIX
        match.command(EXAMPLE)): #Returns True if the message following the prefix begins with EXAMPLE
        print(match.args) #Prints the message, but without PREFIX and without EXAMPLE
bot.add_message_listener(example)
```
The command method will be improved, although with incompatable changes in the next major version of Simple-Major-Bot-Lib.

#### Using the not_from_this_bot method
The not_from_this_bot method of the MessageMatch class can be used to filter messages based on whether they come from Matrix users and not from this bot. not_from_this_bot returns True if the message sender is not the bot. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if match.not_from_this_bot: #Returns True if the message was sent by a different user
        #Do Something
bot.add_message_listener(example)
```

#### Using the contains method
The contains method of the MessageMatch class can be used to filter messages based on whether a specified string is within the message body. An example is shown in the following python code.
```python
async def example(room,message):
    match = botlib.MessageMatch(room, message, bot)
    if match.contains("example string"): #Returns True if the message body contains "example string"
        #Do Something
bot.add_message_listener(example)
```
.. _quickstart:

# Quickstart

[View on Github](https://github.com/KrazyKirby99999/simple-matrix-bot-lib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/)

### Install the simplematrixbotlib package
Simple-Matrix-Bot-Lib's package is simplematrixbotlib. It can be installed from pip or downloaded from github.
Installation from pip:
```
python -m pip install simplematrixbotlib
```
Download from github:
```
git clone --branch master https://github.com/KrazyKirby99999/simple-matrix-bot-lib.git
```

### Obtain Matrix login credentials
Go to https://app.element.io/#/register

If you are already using element web, then you may want to use a private session in your browser.

Change the homeserver if you prefer, and enter a new username, password, and/or email into the respective fields.

Save the homeserver, username, and password at a safe location, then complete the captcha.

Your bot's login credentials should resemble the following:

homeserver: https://example.com

username: example_bot

password: secretpassword

### Create the bot
(Finished example code will be provided in full at the bottom)

Begin by importing packages.
```python
import simplematrixbotlib as botlib
```
Create a Creds object with your login credentials.
```python
creds = botlib.Creds("https://home.server", "user", "pass")
```
Create a bot object. This will be used throughout your project.
```python
bot = botlib.Bot(creds)
```
If you want to use a prefix in the commands that your bot responds to, you may want to define a constant.
```python
PREFIX = '!'
```
Before creating a command, it is necessary to add a listener(callback) for the bot to use it.
```python
@bot.listener.on_message_event
```
Create a command by defining a function. The function must be an "async" function with (room, message) as the arguments.
```python
async def echo(room, message): 
    """
    Example command that "echoes" arguements.
    Usage:
    example_user- !echo say something
    echo_bot- say something
    """
```
Creating a MessageMatch object is optional, but is necessary if you want to use "match filters".
```python
    match = botlib.MessageMatch(room, message, bot) 
```
These match filters will only allow the bot to react to messages that are not from the bot, messages that begin with the prefix, and messages that start with "echo" (following the prefix).
```python
    if match.not_from_this_bot() and match.prefix(PREFIX) and match.command("echo"):
```
This part of the command is the part that "acts". The line provided sends a message to the room of the message that the bot is responding to, and sends a message containing the text following the command in the message using MessageMatch.args.
```python
        await bot.api.send_text_message(room.room_id, match.args) 
```
And finally run the bot.
```python
bot.run()
```
This bot is an echo bot, which "echoes" the arguments of any message that starts with "!echo"(<PREFIX><COMMAND>). As many commands as needed can be added, each with its own function and with its own call of add_message_listener.

Full code of echo bot example
```python
import simplematrixbotlib as botlib
import os

creds = botlib.Creds("https://home.server", "user", "pass")
bot = botlib.Bot(creds)

PREFIX = '!'

@bot.listener.on_message_event
async def echo(room, message):
    """
    Example function that "echoes" arguements.
    Usage:
    example_user- !echo say something
    echo_bot- say something
    """
    match = botlib.MessageMatch(room, message, bot)
    if match.not_from_this_bot() and match.prefix(PREFIX) and match.command("echo"):
        await bot.api.send_text_message(room.room_id, match.args)

bot.run()
```

Other examples can be found [here](examples.html).
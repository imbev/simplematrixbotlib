# Simple-Matrix-Bot-Lib
(Version 1.6.x)

Simple-Matrix-Bot-Lib is a Python bot library for the Matrix ecosystem built on [matrix-nio](https://github.com/poljar/matrix-nio).

[View on Github](https://github.com/KrazyKirby99999/simple-matrix-bot-lib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/) or
[View docs on readthedocs.io](https://simple-matrix-bot-lib.readthedocs.io/en/latest/)

Learn how you can contribute [here](CONTRIBUTING.md).

## Installation

### simplematrixbotlib can be either installed from PyPi or downloaded from github.<br>

Installation from PyPi:

```
python -m pip install simplematrixbotlib
```

Download from github:

```
git clone --branch master https://github.com/KrazyKirby99999/simple-matrix-bot-lib.git
```

## Example Usage

```python
# echo.py
# Example:
# randomuser - "!echo example string"
# echo_bot - "example string"

import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "echo_bot", "pass")
bot = botlib.Bot(creds)
PREFIX = '!'

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):

        await bot.api.send_text_message(
            room.room_id, " ".join(arg for arg in match.args())
            )

bot.run()
```

More examples can be found [here](examples).

## Features

### Complete:

- #### Login to homeserver with password - bot automatically login upon the execution of bot.run()
  
- #### Login to homeserver with token - bot uses token provided via SSO (Single Sign-On) to login

- #### Join room on invite - bot automatically join rooms that the bot is invited to upon execution of bot.run(), or upon invite if the bot is running

- #### Send messages - bot can send messages in response to other messages, and can also run other code in response to messages as well as filter the messages that the bot responds to

- #### Send images - bot can send image messages

- #### Execute action based on criteria - "match filters" can be used to  specify which messages for the bot to respond to

- #### Preserve sessions - Sessions are now preserved between logins. The access token and device id are now saved in sessions.txt, unless specified otherwise.

- #### Add choice of actions to execute at bot login - Execute action after logging in


### In Progress:

- #### Add more examples
- #### Improve Documentation

### Planned:

- #### Add toggles for defaults
- #### Sending of markdown formatted messages
- #### More


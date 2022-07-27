# Simple-Matrix-Bot-Lib
(Version 2.6.3)

Simple-Matrix-Bot-Lib is a Python bot library for the Matrix ecosystem built on [matrix-nio](https://github.com/poljar/matrix-nio).

[View on Github](https://github.com/KrazyKirby99999/simple-matrix-bot-lib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/) or
[View docs on readthedocs.io](https://simple-matrix-bot-lib.readthedocs.io/en/latest/)

Learn how you can contribute [here](CONTRIBUTING.md).

## Installation

### simplematrixbotlib can be either installed from PyPi or downloaded from github.

Installation from PyPi:

```
python -m pip install simplematrixbotlib
```

Download from github:

```
git clone --branch master https://github.com/KrazyKirby99999/simple-matrix-bot-lib.git
```

### install encryption support

The `e2e` extra of `matrix-nio` is required to support encrypted matrix rooms.
In turn, `matrix-nio[e2e]` requires [`libolm`](https://gitlab.matrix.org/matrix-org/olm) version 3.0.0 or newer.
You can install it using you distribution's package manager or from source.
More information is available at [matrix-nio](https://github.com/poljar/matrix-nio#installation).

Finally install e2e support for matrix-nio by running:

```
python -m pip install matrix-nio[e2e]
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

More information and examples can be found [here](https://simple-matrix-bot-lib.readthedocs.io/en/latest/).

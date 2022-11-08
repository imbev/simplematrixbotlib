# Simple-Matrix-Bot-Lib
(Version 2.8.0)

Simple-Matrix-Bot-Lib is a Python bot library for the Matrix ecosystem built on [matrix-nio](https://github.com/poljar/matrix-nio).

[View on Github](https://github.com/i10b/simplematrixbotlib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/) or
[View docs on readthedocs.io](https://simple-matrix-bot-lib.readthedocs.io/en/latest/)

Learn how you can contribute [here](CONTRIBUTING.md).

## Features

- [x] hands-off approach: get started with just 10 lines of code (see [example](#Example-Usage))
- [x] [end-to-end encryption support](https://simple-matrix-bot-lib.readthedocs.io/en/latest/manual.html#e2e-encryption)
- [x] limited [verification support](https://simple-matrix-bot-lib.readthedocs.io/en/latest/manual.html#verification) (device only)
- [x] easily [extensible config file](https://simple-matrix-bot-lib.readthedocs.io/en/latest/manual.html#extending-the-config-class-with-custom-settings)
- [x] [user access management](https://simple-matrix-bot-lib.readthedocs.io/en/latest/manual.html#allowlist)
- [x] access the matrix-nio library to use advanced features

## Installation

### simplematrixbotlib can be either installed from PyPi or downloaded from github.

Installation from PyPi:

```
python -m pip install simplematrixbotlib
```

[Read the docs](https://simple-matrix-bot-lib.readthedocs.io/en/latest/manual.html#e2e-encryption) to learn how to install E2E encryption support.

Download from github:

```
git clone --branch master https://github.com/i10b/simplematrixbotlib.git
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

# Simple-Matrix-Bot-Lib
(Version 2.6.4)

Simple-Matrix-Bot-Lib is a Python bot library for the Matrix ecosystem built on [matrix-nio](https://github.com/poljar/matrix-nio).

[View on Github](https://github.com/i10b/simplematrixbotlib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/) or
[View docs on readthedocs.io](https://simple-matrix-bot-lib.readthedocs.io/en/latest/)

Learn how you can contribute [here](CONTRIBUTING.md).

## Features

- [x] hands-off approach: get started with just 10 lines of code (see [example](#Example-Usage))
- [x] end-to-end encryption support
- [x] limited verification support (device only)
- [x] easily extensible config file
- [x] user access management

## Installation

### simplematrixbotlib can be either installed from PyPi or downloaded from github.

Installation from PyPi:

```
python -m pip install simplematrixbotlib
```

Download from github:

```
git clone --branch master https://github.com/i10b/simplematrixbotlib.git
```

### install encryption support

The `e2e` extra of `matrix-nio` is required to support encrypted matrix rooms.
In turn, `matrix-nio[e2e]` requires [`libolm`](https://gitlab.matrix.org/matrix-org/olm) version 3.0.0 or newer.
You can install it using you distribution's package manager or from source.

[![](https://img.shields.io/static/v1?style=flat-square&label=Ubuntu&message=libolm-dev&color=limegreen)](https://ubuntu.pkgs.org/22.04/ubuntu-universe-amd64/libolm-dev_3.2.10~dfsg-6ubuntu1_amd64.deb.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=Debian&message=libolm-dev&color=limegreen)](https://debian.pkgs.org/11/debian-main-amd64/libolm-dev_3.2.1~dfsg-7_amd64.deb.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=Arch%20Linux&message=libolm&color=limegreen)](https://archlinux.pkgs.org/rolling/archlinux-community-x86_64/libolm-3.2.12-1-x86_64.pkg.tar.zst.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=CentOS&message=libolm-devel&color=limegreen)](https://centos.pkgs.org/8/epel-x86_64/libolm-devel-3.2.10-1.el8.x86_64.rpm.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=Fedora&message=libolm-devel&color=limegreen)](https://fedora.pkgs.org/36/fedora-x86_64/libolm-devel-3.2.10-2.fc36.x86_64.rpm.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=openSUSE&message=olm-devel&color=limegreen)](https://opensuse.pkgs.org/tumbleweed/opensuse-oss-x86_64/olm-devel-3.2.12-1.1.x86_64.rpm.html)

More information is available at [matrix-nio](https://github.com/poljar/matrix-nio#installation).

Finally, install e2e support for matrix-nio by running:

```
python -m pip install matrix-nio[e2e]
```

If there are issues installing the e2e extra with pip from PyPI, additional packages may be required to build python-olm on your distribution, for example python3-devel on openSUSE.

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

### Requirements

End-to-end encryption support requires some additional dependencies to be installed, namely the `e2e` extra of `matrix-nio`.
In turn, `matrix-nio[e2e]` requires [`libolm`](https://gitlab.matrix.org/matrix-org/olm) version 3.0.0 or newer.
You can install it using you distribution's package manager or from source.

[![](https://img.shields.io/static/v1?style=flat-square&label=Ubuntu&message=libolm-dev&color=limegreen)](https://ubuntu.pkgs.org/22.04/ubuntu-universe-amd64/libolm-dev_3.2.10~dfsg-6ubuntu1_amd64.deb.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=Debian&message=libolm-dev&color=limegreen)](https://debian.pkgs.org/11/debian-main-amd64/libolm-dev_3.2.1~dfsg-7_amd64.deb.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=Arch%20Linux&message=libolm&color=limegreen)](https://archlinux.pkgs.org/rolling/archlinux-community-x86_64/libolm-3.2.12-1-x86_64.pkg.tar.zst.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=CentOS&message=libolm-devel&color=limegreen)](https://centos.pkgs.org/8/epel-x86_64/libolm-devel-3.2.10-1.el8.x86_64.rpm.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=Fedora&message=libolm-devel&color=limegreen)](https://fedora.pkgs.org/36/fedora-x86_64/libolm-devel-3.2.10-2.fc36.x86_64.rpm.html)
[![](https://img.shields.io/static/v1?style=flat-square&label=openSUSE&message=olm-devel&color=limegreen)](https://opensuse.pkgs.org/tumbleweed/opensuse-oss-x86_64/libolm3-3.2.12-1.1.x86_64.rpm.html)

More information is available at [matrix-nio](https://github.com/poljar/matrix-nio#installation).

Finally, install e2e support for matrix-nio by running:

```
python -m pip install matrix-nio[e2e]
```

If there are issues installing the e2e extra with pip from PyPI, additional packages may be required to build python-olm on your distribution, for example python3-devel on openSUSE.

### Enabling

Encryption needs to be enabled in simplematrixbotlib's Config before calling `bot.run()`.
When the dependencies are met, it will be enabled automatically but can be turned off if required.

```python
config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = False
config.store_path = './crypto_store/'
bot = botlib.Bot(creds, config)
bot.run()
```

### Configuration Options

See [the Config class manual](#built-in-values) to learn about settings regarding encryption provided by the Config class.

Additionally, you can manage trusted and distrusted devices using nio directly using the following methods.
There are 4 states:
- default: Initially, devices are not trusted. Trying to send a message when such a device is present will cause an Exception, unless `ignore_unverified_devices` is enabled. This state resembles Element's setting "Never send encrypted messages to unverified sessions from this session".
- ignored: Nio will ignore that this device is not verified and send encrypted messages to it regardless. This resembles the default "gray shield" used by Element.
- verified: This is an explicitly trusted device and will receive messages. This resembles the "green shield" in Element.
- blacklisted: This device is explicitly untrusted and will not receive encrypted messages. This resembles the "red shield" in Element.

```python
# set a device's trust state
# verifying a blacklisted or ignored device will automatically remove the former state
bot.async_client.olm.verify_device(device)
bot.async_client.olm.ignore_device(device)
bot.async_client.olm.blacklist_device(device)

# unset a device's trust state
bot.async_client.olm.unverify_device(device)
bot.async_client.olm.unignore_device(device)
bot.async_client.olm.unblacklist_device(device)

# check a device's trust state
bot.async_client.olm.is_device_verified(device)
bot.async_client.olm.is_device_ignored(device)
bot.async_client.olm.is_device_blacklisted(device)
```

### Verification

The library supports 2 common types of verification.

#### Manual "Session key" fingerprint verification

Upon startup, when encryption is enabled, simplematrixbotlib will print some information about its device similar to this:

```
Connected to https://client.matrix.org as @simplematrixbotlib:matrix.org (ABCDEFGHIJKL)
This bot's public fingerprint ("Session key") for one-sided verification is: 0123 4567 89ab cdef ghij klmn opqr stuv wxyz ACBD EFG
```

1. Using the "Session ID" (e.g. `ABCDEFGHIJKL`) given in braces after the bot's Matrix ID and the fingerprint given in the next line, we can proceed to do verify our bot from our Matrix client.
2. In Element Web or Desktop, open the bot user's info and click on "X session(s)" - NOT on "Verify".
3. The bot's current sessions named "Bot Client using Simple-Matrix-Bot-Lib" will be listed with gray shields next to them.
4. Click the session with the correct Session ID, then select "Manually Verify by Text".
5. Confirm that Session ID and Session key shown in Element match those printed by your bot, then click "Verify session".

You have now verified your bot session one-sided from Element.
This means, Element now knows that it really is your bot and be able to detect any attacks and show a red shield.
However, since this is one-sided verification, your bot does not know the same about your Element session.

#### Interactive SAS verification using Emoji

The library is able to perform interactive to-device verification using the SAS method and Emoji.
In-room verification is not supported by nio at this time, thus only single devices can be verified with each other individually.
This method appears **not** to be supported by some clients, such as Element Android, at the time of writing.

Enable this method by the setting provided in the config class:

```python
config.emoji_verify = True
```

Your bot now listens for incoming verification requests.
**Because this method is interactive, you need interactive access to your bot's console!**
Perform the following steps on Element Web/Desktop to verify your session and the bot's session with each other.

1. In Element Web or Desktop, open the bot user's info and click on "X session(s)" - NOT on "Verify".
2. The bot's current sessions named "Bot Client using Simple-Matrix-Bot-Lib" will be listed with gray shields next to them.
3. Click the session with the correct Session ID printed by your bot during startup, then select "Interactively verify by Emoji".
4. Compare the Emoji shown by Element and printed by your bot.
5. Select the appropriate button and enter the appropriate letter into the console depending on whether the Emoji match.

# Changelog

## [v2.6.2](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.6.2)
##  2022-02-26 c432a64
###  Notes:
Fixes a potential security problem.
### Additions:
- None
### Modifications
- Resolve issue [#136](https://github.com/i10b/simplematrixbotlib/issues/136): "Replace usage of ast.literal_eval with json.loads"
### Removals:
- None
### Deprecations
- None

## [v2.6.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.6.1)
### 2022-01-31 d2a3abe2
### Notes:
Fixes a bug.
### Additions:
- None
### Modifications:
- Resolve issue [#129](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/issues/129): "AttributeError: 'Bot' object has no attribute '_need_allow_homeserver_users'"
### Removals:
- None
### Deprecations:
- None

## [v2.6.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.6.0)
### 2022-01-07 46a7be43
### Notes:
Example usage is shown below:
```python
"""
Example Usage:

random_user
      !echo something

random_user2
      *reacts with 👍️

echo_reaction_bot
      Reaction: 👍️
"""

import simplematrixbotlib as botlib

creds = botlib.Creds("https://example.com", "echo_reaction_bot", "password")
bot = botlib.Bot(creds)


@bot.listener.on_reaction_event
async def echo_reaction(room, event, reaction):
    resp_message = f"Reaction: {reaction}"
    await bot.api.send_text_message(room.room_id, resp_message)


bot.run()
```
### Additions:
- A listener for handling `m.reaction` events has been added. Bot developers can now use `Listener.on_reaction_event` to smoothly handle reactions.
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v2.5.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.5.1)
### 2021-12-19 c0e39efa
### Notes:
None
### Additions:
- None
### Modifications:
- Fixed [#101](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/issues/101) 'Api' object has no attribute 'async_client' 
### Removals:
- None
### Deprecations:
- None
## [v2.5.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.5.0)
### 2021-12-17 f636926c
### Notes:
Version 2.5.0 adds improvements to the config feature. A thank you to HarHarLinks for their contributions to version 2.5.0!
### Additions:
- Add allow/block lists: This allows bot developers to specify allow/block lists of users who have permission to interact with the bot using regex.
- Permissions can checked with `Match.is_from_allowed_user()`, which lets the bot developer choose which responses are restricted.
- The allow/block lists can by modified at runtime via the `Config.add_allowlist()`, `Config.remove_allowlist()`, `Config.add_blocklist()`, and `Config.remove_blocklist()` methods.
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v2.4.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.4.1)
### 2021-12-03 e5d6cbd7
### Notes:
Example usage is shown below:
```python
import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")
bot = botlib.Bot(creds)
PREFIX = '!'

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command( "echo"):
        response = " ".join(arg for arg in match.args())
        await bot.api.send_text_message(room.room_id, response)

bot.run()
```
A thank you to HarHarLinks for their contributions to version 2.4.1!
### Additions:
- (Documentation) Added missing `await` statements to several examples
- (Documentation) Added additional clarification on using the `m.notice` msgtype
### Modifications:
- (Documentation) Used Markdown instead of HTML to display a specific link
### Removals:
- None
### Deprecations:
- None
## [v2.4.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.4.0)
### 2021-11-25 ad463210
### Notes:
Version 2.4.0 provides several new features and a fix. A thank you to HarHarLinks for their contributions to version 2.4.0!
Example usage is shown below:
```python
import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")
bot = botlib.Bot(creds)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command(
            "echo"):
            
        response = " ".join(arg for arg in match.args())
        await bot.api.send_text_message(room.room_id, response, "m.notice") ## Uses the msgtype of m.notice instead of m.text

bot.run()
```
### Additions:
- Newlines are now supported when sending markdown messages.
- The msgtype of text and markdown messages can now be specified. Text and markdown messages can now optionally be sent as `m.notice` to avoid alerting everybody of the new message. The default msgtype will continue to be `m.text`.
### Modifications:
- Fixed issue where the homeserver was hardcoded in an http request.
### Removals:
- None
### Deprecations:
- None
## [v2.3.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.3.0)
### 2021-11-18 cda56a46
### Notes:
Version 2.3.0 adds support for additional configuration via config files and other methods. Currently, there is only one setting that can be changed, however many existing and future features will be able to be enabled or disabled via this config.
Example usage is shown below:
```python
"""
random_user
     !echo something
echo_bot
     something
"""

import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")

config = botlib.Config()
config.load_toml("config.toml")

bot = botlib.Bot(creds, config)
PREFIX = '!'

@bot.listener.on_message_event
async def echo(room, message):
     match = botlib.MessageMatch(room, message, bot, PREFIX)

     if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):
          await bot.api.send_text_message(room.room_id,
                                " ".join(arg for arg in match.args()))

bot.run()
```
An example of a toml config file is shown below:
```toml
[simplematrixbotlib.config]
join_on_invite = false
```
### Additions:
- Configuration via config files and other methods.
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v2.2.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.2.0)
### 2021-11-08 96b120e9
In addition to username/access_token, it is possible to authenticate using username/password and login(SSO) token.
Example usage is shown below:
```python
"""
Example Usage:

random_user
      !echo something

echo_bot
      something
"""

import simplematrixbotlib as botlib

creds = botlib.Creds(
    homeserver="https://example.org",
    username="echo_bot",
    access_token="syt_c2...DTJ",
    )
bot = botlib.Bot(creds)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command(
            "echo"):

        await bot.api.send_text_message(room.room_id,
                                        " ".join(arg for arg in match.args()))


bot.run()
```
### Additions:
- Aauthentication via access_tokens
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v2.1.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.1.0)
### 2021-08-27 29b70539
### Notes:
Example usage is shown below:
```python
#### Respond to all messages from users with a hello world message that involves markdown formatting

import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")

bot = botlib.Bot(creds)

@bot.on_message_event

async def hello_world_md(room, message):
    match = botlib.MessageMatch(room, message, bot)

    markdown_message = "# Hello World from [simplematrixbotlib](https://github.com/KrazyKirby99999/simple-matrix-bot-lib)!"
    if match.is_not_from_this_bot():

        await bot.api.send_markdown_message(
            room_id=room.room_id,

            message=markdown_message)

bot.run()
```
### Additions:
- Send messages formatted in markdown via the `Bot.api.send_markdown_message()` method.
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v2.0.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v2.0.0)
### 2021-08-24 bdd767bb
### Notes:
The second major version of the simplematrixbotlib package has been released.
Example usage is shown below:
```python
#### echo.py
#### Example:

#### randomuser - "!echo example string"
#### echo_bot - "example string"

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
### Additions:
- `Bot.listener`
- `Listener.on_message_event`
- `Listener.on_custom_event`
- `Listener.on_startup`
- `MessageMatch.args`
- `MessageMatch.is_from_userid`
- Login via login_token
### Modifications:
- Rename `MessageMatch.not_from_this_bot` to `MessageMatch.is_not_from_this_bot`
- `MessageMatch.command` Return string if no arguments passed
### Removals:
- `Bot.add_message_listener`
- `Bot.add_startup_action`
### Deprecations:
- None
## [v1.6.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.6.1)
### 2021-08-07 3ef235e4
### Notes:
Final release of v1
### Additions:
- None
### Modifications:
- Fix dependency error upon package installation 
### Removals:
- None
### Deprecations:
- None
## [v1.6.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.6.0)
### 2021-08-01 1e2d5f9
### Notes:
None
### Additions:
- Sending images via `bot.api.send_image_message`
### Modifications:
- Fix a bug in which the bot would print the join message twice
### Removals:
- None
### Deprecations:
- None
## [v1.5.3](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.5.3)
### 2021-07-31 adcf81dc
### Notes:
None
### Additions:
- None
### Modifications:
-  Fix extra join message bug
### Removals:
- None
### Deprecations:
- None
## [v1.5.2](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.5.2)
### 2021-07-10 f5051ceb
### Notes:
None
### Additions:
- None
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v1.5.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.5.1)
### 2021-06-15 4f5cb8f1
### Notes:
No changes to functionality or API
### Additions:
- None
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v1.5.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.5.0)
### 2021-06-14 039ceef4
### Notes:
None
### Additions:
- `Bot.add_startup_action`
### Modifications:
- Fix getting of joined rooms
### Removals:
- None
### Deprecations:
- None
## [v1.4.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.4.0)
### 2021-06-14 8da3a618
### Notes:
None
### Additions:
- Use stored device_name and access_token to login
### Modifications:
- Fix decryption of access_token and device_id
- Refactor `Creds` class
### Removals:
- None
### Deprecations:
- None
## [v1.3.3](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.3.3)
### 2021-06-11 9e382067
### Notes:
None
### Additions:
- None
### Modifications:
- Rename `API` class to `Api`
- Add numpy-style docstrings
### Removals:
- None
### Deprecations:
- None
## [v1.3.2](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.3.2)
### 2021-06-08 7db56306
### Notes:
None
### Additions:
- None
### Modifications:
-  Fix inaccurate command matching
### Removals:
- None
### Deprecations:
- None
## [v1.3.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.3.1)
### 2021-06-07 aef4748a
### Notes:
None
### Additions:
- None
### Modifications:
- Ignore messages sent before bot run 
### Removals:
- None
### Deprecations:
- None
## [v1.3.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.3.0)
### 2021-06-07 08cf8897
### Notes:
None
### Additions:
- Matching messages via `MessageMatch` class
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v1.2.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.2.0)
### 2021-06-06 94786fd7
### Notes:
None
### Additions:
- `Bot.add_message_listener`
- `API.send_text_message`
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None
## [v1.1.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.1.0)
### 2021-06-05 6f74ce1b
### Notes:
None
### Additions:
- None
### Modifications:
- Implement callbacks into Bot
- Refactor asyncio loop 
### Removals:
- None
### Deprecations:
- None
## [v1.0.1](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.0.1)
### 2021-06-04 6640e325
### Notes:
None
### Additions:
- None
### Modifications:
- Add additional keywords to setup.py 
### Removals:
- None
### Deprecations:
- None
## [v1.0.0](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/releases/tag/v1.0.0)
### 2021-06-04 1197bda4
### Notes:
Initial Release
### Additions:
- None
### Modifications:
- None
### Removals:
- None
### Deprecations:
- None

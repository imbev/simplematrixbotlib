# Quickstart

[View on Codeberg](https://codeberg.org/imbev/simplematrixbotlib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/)



### Install the simplematrixbotlib package
Installation from pip:
```
python3 -m pip install simplematrixbotlib
```
Download git repository:
```
git clone https://codeberg.org/imbev/simplematrixbotlib.git
```

### Obtain Matrix login credentials
1. Go to [Element Web](https://app.element.io/#/register)

2. If you are already using element web, then you may want to use a private session in your browser.

3. Change the homeserver if you prefer, and enter a new username, password, and/or email into the respective fields.

4. Save the homeserver, username, and password at a safe location, then complete the captcha.

Your bot's login credentials should resemble the following:

```txt
homeserver: https://example.com

username: example_bot

password: secretpassword
```

### Create the bot
(The example source code will be provided in full at the bottom)

Begin by importing the package.
```python
import simplematrixbotlib as botlib
```
Create a Creds object with your login credentials.
```python
creds = botlib.Creds("https://home.server", "user", "pass")
```
Create a bot object. This will be used as a handle throughout your project.
```python
bot = botlib.Bot(creds)
```
If you want to use a prefix in the commands that your bot responds to, it may be useful to assign it to a variable.
```python
PREFIX = '!'
```
Before creating a function handler for a command, it is necessary to add a listener.
```python
@bot.listener.on_message_event
```
Create a command by defining a function. The function must be an "async" function with two arguments. Recommended argument names are (room, message) or (room, event)
```python
async def echo(room, message): 
    """
    Example command that "echoes" arguements.
    Usage:
    example_user- !echo say something
    echo_bot- say something
    """
```
Creating a MessageMatch object is optional, but useful for handling messages. The prefix argument is optional, but is needed when matching prefixes.
```python
    match = botlib.MessageMatch(room, message, bot, PREFIX) 
```
This specific usage of the MessageMatch class will only allow the bot to react to messages that are not from the bot and also start with "!echo".
```python
    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):
```
This part of the handler is responsible for sending the response message. The rest of the message following "!echo" will be sent to the same room as the message.
```python
        await bot.api.send_text_message(room.room_id, " ".join(arg for arg in match.args())) 
```
Finally run the bot.
```python
bot.run()
```
This bot is an echo bot, which "echoes" the arguments of any message that starts with "!echo"(<PREFIX><COMMAND>). As many handlers as needed can be added, each with its own handler function and a listener.

Full code of echo bot example
```python
import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")
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

Other examples can be found [here](examples.md).
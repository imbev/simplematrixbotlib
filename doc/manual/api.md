### How to use the Api class
The Api class is a class that is used to simplify interaction with the matrix-nio library that Simple-Matrix-Bot-Lib is built upon. The source is located at simplematrixbotlib/api.py

### Accessing an Api instance
An instance of the Api class is automatically created when an instance of the Bot class is created. An example is shown in the following python code.
```python
bot = botlib.Bot(creds)
bot.api #Instance of the Api class
```

### Using the send_text_message method
The send_text_message method of the Api class can be used to send text messages in Matrix rooms. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_message = "Hello World"
    if match.is_not_from_this_bot():
        await bot.api.send_text_message(
            room_id=room.room_id,
            message=example_message)
```
The first two arguments are required. The room_id argument is the id of the destination room. The message argument is the string that is to be sent as a message.

#### Sending a bot notice
To send a bot notice (non-alerting message), set the argument `msgtype="m.notice"`. It can be combined with any of the other optional arguments.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_message = "Hello World"
    if match.is_not_from_this_bot():
        await bot.api.send_text_message(
            room_id=room.room_id,
            message=example_message,
            msgtype="m.notice")
```

#### Sending a reply
To send your message as a reply to another message, pass the original message event to the `reply_to` argument. It can be combined with any of the other optional arguments.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_message = "Hello World"
    if match.is_not_from_this_bot():
        await bot.api.send_text_message(
            room_id=room.room_id,
            message=example_message,
            reply_to=message)
```

#### Sending a markdown formatted message
To translate markdown in your `example_message` into a HTML formatted message, set the argument `markdown=True`. It can be combined with any of the other optional arguments.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_message = "Hello World"
    if match.is_not_from_this_bot():
        await bot.api.send_text_message(
            room_id=room.room_id,
            message=example_message,
            markdown=True)
```

Alternatively, use the send_markdown_message alias method, which also supports the other optional arguments:
```python
await bot.api.send_markdown_message(
    room_id=room.room_id,
    message=example_markdown,
    msgtype="m.notice",
    reply_to=message)
```

### Using the send_image_message method
The send_image_message method of the Api class can be used to send image messages in Matrix rooms. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_image="./img/example.png"
    if match.is_not_from_this_bot():
        await bot.api.send_image_message(
            room_id=room.room_id,
            image_filepath=example_image)
```
Both arguments are required. The room_id argument is the id of the destination room. The image_filepath argument is a string that is the path to the image file that is to be sent as a message.

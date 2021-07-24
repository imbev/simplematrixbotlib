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
    if match.not_from_this_bot():
        bot.api.send_text_message(
            room_id=room.room_id, 
            message=example_message)
```
Both arguments are required. The room_id argument is the id of the destination room. The message argument is the string that is to be sent as a message.

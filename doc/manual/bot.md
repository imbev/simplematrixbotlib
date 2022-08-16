The Bot class is a class that handles most of the functionality of a bot created with Simple-Matrix-Bot-Lib. The source is located at simplematrixbotlib/bot.py.

### Creating an instance of the Bot class
An instance can be created using the following python code.
```python
bot = botlib.Bot(
    creds=creds,
    config=config
    )
```
The creds argument is neccesary, and is an instance of the Creds class. The config argument is optional, and is an instance of the Config class.

### Running the Bot
When the Bot is ready to be started, the run method can be used to run the Bot. An example is shown in the following python code.
```
bot.run()
```

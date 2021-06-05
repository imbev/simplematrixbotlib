# Simple-Matrix-Bot-Lib
(Version 1.1.x)

simplematrixbotlib is a Python 3 library for quickly building Matrix bots. It uses [matrix-nio](https://github.com/poljar/matrix-nio) as its Matrix client library.
[View on Github](https://github.com/KrazyKirby99999/simple-matrix-bot-lib) or [View on PyPi](https://pypi.org/project/simplematrixbotlib/)
# Installation
### To use it, simplematrixbotlib can be either installed from pip or downloaded from github.</br>
Installation from pip:
```
python -m pip install simplematrixbotlib
```
Download from github:
```
git clone --branch master https://github.com/KrazyKirby99999/simple-matrix-bot-lib.git
```

# Example Usage
```python
import simplematrixbotlib as botlib
    
creds = botlib.Creds("home.server", "user", "pass")
bot = botlib.Bot(creds)
bot.run()
```

# Features
## Complete:
- ### Login to homeserver - Bots automatically login upon the execution of bot.run() 
    ```python
    import simplematrixbotlib as botlib
    
    creds = botlib.Creds("home.server", "user", "pass")
    bot = botlib.Bot(creds)
    bot.run() #Logs in during the execution of this line
    ```
- ### Join room on invite - Bots automatically join rooms that the bot is invited to upon execution of bot.run(), or upon invite if the bot is running

## In Progress:
- ### Execute action based on criteria
- ### Send message

## Planned:
- ### More

# Dependencies
## Python:
- ### matrix-nio >= 0.18.2
## External:
- ### Python >= 3.7

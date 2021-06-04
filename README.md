# Simple-Matrix-Bot-Lib
(Version 0.0.2)

simplematrixbotlib is a Python 3 library for quickly building Matrix bots. It uses [matrix-nio](https://github.com/poljar/matrix-nio) as its Matrix client library.

# Installation
### To use it, simplematrixbotlib can be either installed from pip or downloaded from github.</br>
Installation from pip:
```
python -m pip install simplematrixbotlib
```
Installation from github:
```
git clone https://github.com/KrazyKirby99999/simple-matrix-bot-lib.git
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
- ### Login to Matrix - Bots automatically login to matrix upon the execution of bot.run() 
    ```python
    import simplematrixbotlib as botlib
    
    creds = botlib.Creds("home.server", "user", "pass")
    bot = botlib.Bot(creds)
    bot.run() #Logs in during the execution of this line
    ```

## In Progress:
- ### N/A

## Planned:
- ### Join room on invite
- ### Execute action if messages meet criteria
- ### Send message
- ### More

# Dependencies
## Python:
- ### matrix-nio >= 0.18.2
## External:
- ### Python >= 3.7
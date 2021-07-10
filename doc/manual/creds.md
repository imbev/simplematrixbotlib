### How to use the Creds class
The Creds class is a class that handles login credentials. The source is located at simplematrixbotlib/auth.py.

#### Creating an instance of the Creds class
An instance can be created using the following python code.
```
creds = botlib.Creds(
    homeserver="https://example.org", 
    username="username", 
    password="password", 
    session_stored_file="session.txt"
    )
```
The homeserver, username, and password arguments are strings, self explanatory and are always neccesary when creating an instance. The session_stored_file argument is optional and allows for specific data relating to each session such as the access token and the device name to be preserved across each run of the bot.
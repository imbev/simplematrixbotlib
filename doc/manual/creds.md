### How to use the Creds class
The Creds class is a class that handles login credentials. The source is located at simplematrixbotlib/auth.py.

#### Creating an instance of the Creds class
An instance can be created using the following python code.
```python
creds = botlib.Creds(
    homeserver="https://example.org", 
    username="username", 
    password="password", 
    session_stored_file="session.txt"
    )
```
or
```python
creds = botlib.Creds(
    homeserver="https://example.org", 
    login_token="MDA..gZ2"
    session_stored_file="session.txt"
    )
```
The homeserver argument is always required. The username, and password arguments are also required unless the login_token argument is used. The keyword "login_token" must be specified when the login_token argument is used. Although the login_token can only be used to authenticate with the homeserver once, it is required in every run of the bot in order to encrypt/decrypt the session data such as the access_token. If the login_token is used and the session_stored_file argument is set to `None`, then the bot will only be able to run once per login_token. The session_stored_file argument is optional and allows for specific data relating to each session such as the access token and the device name to be preserved across each run of the bot.
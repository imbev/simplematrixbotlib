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
    username="username", 
    login_token="MDA..gZ2",
    session_stored_file="session.txt"
    )
```
or
```python
creds = botlib.Creds(
    homeserver="https://example.org",
    username="username",
    access_token="syt_c2...DTJ",
    session_stored_file="session.txt"
    )
```
The homeserver and username arguments are always required.  The password argument may be replaced by either the login_token argument or the access_token argument. The login_token is used with handling SSO logins (See the [Matrix Docs](https://matrix.org/docs/guides/sso-for-client-developers#handling-sso)). The access_token is normally generated after using a different login method with another client. 

The optional session_stored_file argument is the location of a file used by the bot to store session information such as the generated access token and device name. A login_token can only be used to authenticate once, so setting the session_stored_file argument to "" will require you to enter a new SSO token each time the program is run.
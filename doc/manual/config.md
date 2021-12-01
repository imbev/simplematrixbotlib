### How to use the Config class
The Config class is a class that handles whether certain features are enabled or disabled. The source is located at simplematrixbotlib/config.py

#### Supported Values
##### `join_on_invite`
Boolean: whether the bot accepts all invites automatically.

##### `allowlist`
List of strings: [Regular expressions](https://docs.python.org/3/library/re.html) of matrix user IDs who are allowed to send commands to the bot.
Defaults to allow everyone on the bot's homeserver.
If the list is non-empty, user IDs that are not on it are blocked. Thus to allow anybody, set it to `[]`.
You can check using `Match.is_from_allowed_user` if the sender of a command is allowed to use the bot and act accordingly.

##### `blocklist`
List of strings: [Regular expressions](https://docs.python.org/3/library/re.html) of matrix user IDs who are not allowed to send commands to the bot.
Defaults to empty, blocking nobody.
Blocks user IDs on it if non-empty, even overriding the `allowlist`.
For example: this way it is possible to allow all users from a homesever, but block single ones.
You can check using `Match.is_from_allowed_user` if the sender of a command is allowed to use the bot and act accordingly.

#### Creating an instance of the Config class
An instance can be created using the following python code.
```python
creds = botlib.Config()
```

#### Reading config values from file
Configuration settings can be set to values read from a file using the following python code.
```
config.load_toml("config.toml")
```
Depending on the file format, a specific method may be used for reading the file. A table of the appropriate method to use for each format is shown below.

| Format | Method            |
|--------|-------------------|
| TOML   | `load_toml(file)` |

Example configuration files for each file format can be under the examples section of the documentation. An example of a toml config file can be found [here](https://simple-matrix-bot-lib.readthedocs.io/en/latest/examples.html#bot-config-file-in-toml-format).

#### Manually setting config values
Configuration settings can also be set manually using the following python code.
```
config.set_join_on_invite(False)
```
Depending on the setting, a specific method may be used for choosing the value. A table of the appropriate method to use for each setting is shown below.

| Method                      | Description                                  |
|-----------------------------|----------------------------------------------|
| `set_join_on_invite(boolean)` | Whether the bot should automatically join rooms on invite. |
| `set_allowlist(list)` | Set the list of users who are allowed to interact with the bot. |
| `add_allowlist(list)` | Merge this list into the list of users who are allowed to interact with the bot. |
| `set_blocklist(list)` | Set the list of users who are disallowed to interact with the bot. |
| `add_blocklist(list)` | Merge this list into the list of users who are disallowed to interact with the bot. |

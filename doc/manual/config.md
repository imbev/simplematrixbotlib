### How to use the Config class
The Config class is a class that handles whether certain features are enabled or disabled. The source is located at simplematrixbotlib/config.py

#### Creating an instance of the Config class
An instance can be created using the following python code.
```python
config = botlib.Config()
```

#### Supported Values

The following Config values may implement validation logic. They can be interacted with as if they were public member variables:
```python
config.join_on_invite = True
print(c.join_on_invite)
```

See also: [Additional Methods](#additional-methods)

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

#### Additional methods
Configuration settings can additionally be manipulated in special ways using the following methods.

| Method                   | Description                                                                            |
|--------------------------|----------------------------------------------------------------------------------------|
| `add_allowlist(list)`    | Merge this list into the list of users who are allowed to interact with the bot.       |
| `remove_allowlist(list)` | Subtract this list from the list of users who are allowed to interact with the bot.    |
| `add_blocklist(list)`    | Merge this list into the list of users who are disallowed to interact with the bot.    |
| `remove_blocklist(list)` | Subtract this list from the list of users who are disallowed to interact with the bot. |

#### Loading and saving config values
Configuration settings can be set to values read from a file using the following python code.
```python
config.load_toml("config.toml")
```
Depending on the file format, a specific method may be used for reading the file. A table of the appropriate method to use for each format is shown below.

| Format | Method            |
|--------|-------------------|
| TOML   | `load_toml(file)` |

Similarly, settings can be written to file after manipulating them at runtime.
```python
config.save_toml("config.toml")
```

| Format | Method            |
|--------|-------------------|
| TOML   | `save_toml(file)` |

Example configuration files for each file format can be under the examples section of the documentation. An example of a toml config file can be found [here](https://simple-matrix-bot-lib.readthedocs.io/en/latest/examples.html#bot-config-file-in-toml-format).

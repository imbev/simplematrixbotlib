### How to use the Config class
The Config class is a class that handles whether or not certain features are enabled or disabled. The source is located at simplematrixbotlib/config.py

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

| Format | Method          |
|--------|-----------------|
| TOML   | load_toml(file) |

#### Manually setting config values
Configuration settings can also be set manually using the following python code.
```
config.set_join_on_invite(False)
```
Depending on the setting, a specific method may be used for choosing the value. A table of the appropriate method to use for each setting is shown below.

| Method                      | Description                                  |
|-----------------------------|----------------------------------------------|
| set_join_on_invite(boolean) | Whether the bot should automatically join rooms on invite. |

The Config class is a class that handles whether certain features are enabled or disabled.
The source is located at simplematrixbotlib/config.py

### Creating an instance of the Config class
An instance can be created using the following python code.
```python
config = botlib.Config()
```

### Built-in Values

The following Config values are may implement validation logic.
They can be interacted with as if they were public member variables:
```python
config.join_on_invite = True
print(config.join_on_invite)
```

See also: [Additional Methods](#additional-methods)

#### `join_on_invite`
Boolean: whether the bot accepts all invites automatically.
Boolean: whether to enable encryption.
Other settings depend on the value of this setting, e.g. setting encryption to false will also set `emoji_verify` to false.
Encryption requires additional encryption-specific dependencies to be installed.

#### `emoji_verify`
Boolean: whether the bot's built-in emoji verification callback should be enabled.
Requires encryption to be enabled.
Learn more at [Interactive SAS verification using Emoji](#interactive-sas-verification-using-emoji).

#### `ignore_unverified_devices`
Boolean: whether to automatically ignore unverified devices in order to send encrypted messages to them without verifying.
See [Encryption Configuration Options](#configuration-options) to learn more about the different trust states, including ignoring.
When encryption is not enabled, messages will always be sent to all devices.

#### `store_path`
String: path in the filesystem where the crypto-session gets stored.
Can be relative (`./store/`) or absolute (`/home/example`).
Needs to be readable and writable by the bot.

#### `allowlist`
List of strings: [Regular expressions](https://docs.python.org/3/library/re.html) of matrix user IDs who are allowed to send commands to the bot.
Defaults to allow everyone on the bot's homeserver.
If the list is non-empty, user IDs that are not on it are blocked.
Thus to allow anybody, set it to `[]`.
You can check using `Match.is_from_allowed_user` if the sender of a command is allowed to use the bot and act accordingly.
**IMPORTANT**: This only applies to `Match.is_from_allowed_user`!

#### `blocklist`
List of strings: [Regular expressions](https://docs.python.org/3/library/re.html) of matrix user IDs who are not allowed to send commands to the bot.
Defaults to empty, blocking nobody.
Blocks user IDs on it if non-empty, even overriding the `allowlist`.
For example: this way it is possible to allow all users from a homeserver, but block single ones.
You can check using `Match.is_from_allowed_user` if the sender of a command is allowed to use the bot and act accordingly.
**IMPORTANT**: This only applies to `Match.is_from_allowed_user`!

### Additional methods
Configuration settings can additionally be manipulated in special ways using the following methods.

| Method                   | Description                                                                            |
|--------------------------|----------------------------------------------------------------------------------------|
| `add_allowlist(list)`    | Merge this list into the list of users who are allowed to interact with the bot.       |
| `remove_allowlist(list)` | Subtract this list from the list of users who are allowed to interact with the bot.    |
| `add_blocklist(list)`    | Merge this list into the list of users who are disallowed to interact with the bot.    |
| `remove_blocklist(list)` | Subtract this list from the list of users who are disallowed to interact with the bot. |

### Loading and saving config values
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

### Extending the Config class with custom settings

The Config class is designed to be easily extensible with any custom field you may need for your specific bot.
This allows you to simply add your settings to the existing bot config file, right next to the other settings.

Extending the Config class is done by deriving your own Config class from it and adding your new values as well as functions if required.

First create your new class, called `MyConfig` for example, based on Config.
Because Config is a dataclass, you need to add the dataclass decorator to your class as well.
Then add your new custom field by adding an attribute to your class, and make sure to add a [type annotation so it gets properly picked up as a dataclass field](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass).
When creating a simple attribute like that, its name may not start with an underscore `_` in order to make it save and load properly.

```python
import simplematrixbotlib as botlib
from dataclasses import dataclass


@dataclass
class MyConfig(botlib.Config):
    custom_setting: str = "My setting"
```

It is possible to add additional logic to your new setting by adding getter and setter methods.
Most built-in settings are implemented this way similar to the example below.

Create your custom field by adding a "private" attribute to your class, i.e. its name starts with an underscore `_`.
Then add a getter method by using the `@property` decorator, and a setter method using the setter decorator `@name-of-your-field-without-underscore.setter`.
The name for each function is also the name of your field without the leading underscore.
Your setting can then be accessed publicly by using the name without underscore, similar to the default Config settings.
The functions for loading and saving your config file will automatically use the getter and setter methods and apply any logic in them.

If you wanted, you could add additional methods, e.g. to implement behavior like that of [`add_allowlist()` etc.](#additional-methods)
Take a look at the Config class source code if you are unsure how to do this.

```python
import simplematrixbotlib as botlib
from dataclasses import dataclass


@dataclass
class MyConfig(botlib.Config):
    _my_setting: str = "Hello"

    @property
    def my_setting(self) -> str:
        return self._my_setting

    @my_setting.setter
    def my_setting(self, value: str) -> None:
        # validate(value)
        self._my_setting = value
```

Finally, use your custom Config class by instantiating it and passing the instance when creating your Bot instance.

```python
config = MyConfig()
config.load_toml('config.toml')
bot = botlib.Bot(creds, config)
```

A complete example implementation of a custom Config class can be found [here](https://simple-matrix-bot-lib.readthedocs.io/en/latest/examples.html#bot-using-custom-option-config-file).

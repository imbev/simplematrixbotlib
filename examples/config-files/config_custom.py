"""
Example Usage:

random_user
      !get

echo_bot
      something
"""

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
        self._my_setting = value


creds = botlib.Creds("https://home.server", "user", "pass")
config = MyConfig()
config.load_toml('config_custom.toml')
bot = botlib.Bot(creds, config)
PREFIX = '!'


@bot.listener.on_message_event
async def get(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command(
            "get"):

        await bot.api.send_text_message(room.room_id, config.my_value)


bot.run()

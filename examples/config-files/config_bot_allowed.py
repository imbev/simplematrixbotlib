"""
Example Usage:

admin1
      !echo something

echo_bot
      something

admin2
      !echo something

user1
      !echo something
"""

import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")

config = botlib.Config()
config.load_toml("config.toml")

bot = botlib.Bot(creds, config)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() \
       and match.is_from_allowed_user() \
       and match.prefix() \
       and match.command("echo"):

        await bot.api.send_text_message(room.room_id,
                                        " ".join(arg for arg in match.args()))


bot.run()

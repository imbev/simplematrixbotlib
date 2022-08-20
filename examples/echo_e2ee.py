"""
Example Usage:

random_user
      *emoji verification or one-sided verification

random_user
      !echo something

echo_bot
      something
"""

import simplematrixbotlib as botlib

config = botlib.Config()
# config.encryption_enabled = True  # Automatically enabled by installing encryption support
config.emoji_verify = True
config.ignore_unverified_devices = True

creds = botlib.Creds("https://home.server", "user", "pass")
bot = botlib.Bot(creds, config)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot()\
            and match.prefix()\
            and match.command("echo"):

        await bot.api.send_text_message(room.room_id,
                                        " ".join(arg for arg in match.args()))


bot.run()

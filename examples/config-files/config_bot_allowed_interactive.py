"""
Example Usage:
note the escaped dot (\.)

user1
      !allow @user2:example\.org

admin1
      !allow @user1:example\.org, @admin2:example\.org

echo_bot
      allowing @user1:example\.org, @admin2:example\.org

user1
      !allow @user2:example\.org

echo_bot
      allowing @user1:example\.org

admin2
      !disallow @user1:example\.org
"""

import simplematrixbotlib as botlib

creds = botlib.Creds("https://home.server", "user", "pass")

config = botlib.Config()
config.load_toml("config_allow_interactive.toml")

bot = botlib.Bot(creds, config)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() \
       and match.is_from_allowed_user() \
       and match.prefix():

        if match.command("allow"):
            bot.config.add_allowlist(set(match.args()))
            await bot.api.send_text_message(room.room_id,
                                            f'allowing {", ".join(arg for arg in match.args())}')

        if match.command("disallow"):
            bot.config.remove_allowlist(set(match.args()))
            await bot.api.send_text_message(room.room_id,
                                            f'disallowing {", ".join(arg for arg in match.args())}')


bot.run()

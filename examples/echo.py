import os

creds = botlib.Creds("https://example.org", "echo_bot", "secretpassword")
bot = botlib.Bot(creds)

prefix = '!'

async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if match.not_from_this_bot() and match.prefix(prefix) and match.command("echo"):
        await bot.api.send_text_message(room.room_id, match.args)

bot.add_message_listener(echo)

bot.run()


# random_user
#       !echo something
#
# echo_bot
#       something
 
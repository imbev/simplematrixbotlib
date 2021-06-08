import os

creds = botlib.Creds("https://example.org", "hight_five_bot", "secretpassword")
bot = botlib.Bot(creds)

PREFIX = '!'

try:
    with open("high_fives.txt", "r") as f:
        bot.total_high_fives = int(f.read())
except FileNotFoundError:
    bot.total_high_fives = 0

async def bot_help(room, message):
    bot_help_message = f"""
    Help Message:
        prefix: {PREFIX}
        commands:
            help:
                command: help, ?, h
                description: display help command
            give high fives:
                command: high_five, hf
                description: high-five the bot!
            count:
                command: count, how_many, c
                description: show amount of high fives
                """
    match = botlib.MessageMatch(room, message, bot)
    if match.not_from_this_bot() and match.prefix(PREFIX) and (
        match.command("help") or match.command("?") or match.command("h")):
            await bot.api.send_text_message(room.room_id, bot_help_message)

bot.add_message_listener(bot_help)

async def high_five(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if match.not_from_this_bot() and match.prefix(PREFIX) and (
        match.command("high_five") or match.command("hf")):

        bot.total_high_fives += 1
        with open("high_fives.txt", "w") as f:
            f.write(str(bot.total_high_fives))
        
        await bot.api.send_text_message(room.room_id, f"{message.sender} high-fived the bot!")

bot.add_message_listener(high_five)

async def high_five_count(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if match.not_from_this_bot and match.prefix(PREFIX) and (
    match.command("count") or match.command("how_many") or match.command("c")):
        await bot.api.send_text_message(room.room_id, f"The bot has been high-fived {str(bot.total_high_fives)} times!")

bot.add_message_listener(high_five_count)

bot.run()

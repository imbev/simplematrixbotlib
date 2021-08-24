import simplematrixbotlib as botlib
import os
import random

creds = botlib.Creds("https://example.org", "echo_bot", "secretpassword")
bot = botlib.Bot(creds)

PREFIX = '!'


@bot.listener.on_message_event
async def help_message(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if not (match.is_not_from_this_bot() and match.prefix()
            and match.command("help")):
        return

    message = (f"""
    Help
    ============================
    What is this bot?
        Rock Paper Scissors Bot is a Matrix bot that plays rock paper scissors with room members and is written in Python using the simplematrixbotlib package.
    Commands?
        {PREFIX}help - show this message
        {PREFIX}play <rock/paper/scissors> - play the game by making a choice
    """)

    await bot.api.send_text_message(room.room_id, message)


@bot.listener.on_message_event
async def make_choice(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    if not (match.is_not_from_this_bot() and match.prefix()
            and match.command("play")):
        return

    temp = True
    if not match.args():
        temp = False
    elif "rock" == match.args()[0]:
        choice = "rock"
    elif "paper" == match.args()[0]:
        choice = "paper"
    elif "scissors" == match.args()[0]:
        choice = "scissors"
    else:
        temp = False

    victory_table = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

    if temp:
        bot_choice = random.choice(["rock", "paper", "scissors"])

        await bot.api.send_text_message(room.room_id, f"You choose {choice}.")
        await bot.api.send_text_message(room.room_id,
                                        f"The bot chose {bot_choice}.")

        if choice == bot_choice:
            await bot.api.send_text_message(room.room_id, "You Tied!")
        if bot_choice == victory_table[choice]:
            await bot.api.send_text_message(room.room_id, "You Won!")
        if choice == victory_table[bot_choice]:
            await bot.api.send_text_message(room.room_id, "You Lost!")

    else:
        await bot.api.send_text_message(
            room.room_id,
            "Invalid choice. Please choose \"rock\", \"paper\", or \"scissors\"."
        )


bot.run()

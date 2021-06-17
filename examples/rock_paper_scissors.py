"""
Example Usage:

random_user
    !help

rock_paper_scissors_bot
    Rock Paper Scissors Bot Help
    ============================
    What is this bot?
        Rock Paper Scissors Bot is a Matrix bot that plays rock paper scissors with room members and is written in Python using the simplematrixbotlib package.
    Commands?
        !help - show this message
        !play <rock/paper/scissors> - play the game by making a choice

random_user
    !play paper

rock_paper_scissors_bot
    You choose paper.
    The bot chose rock.
    You Won!

"""

import simplematrixbotlib as botlib
import os
import random

creds = creds = botlib.Creds("https://example.org", "rock_paper_scissors_bot", "secretpassword")
bot = botlib.Bot(creds)

PREFIX = '!'

async def help_message(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if not (
        match.not_from_this_bot() and match.prefix(PREFIX) and match.command("help")
    ):
        return
    
    message = (
    f"""
    Help
    ============================
    What is this bot?
        Rock Paper Scissors Bot is a Matrix bot that plays rock paper scissors with room members and is written in Python using the simplematrixbotlib package.
    Commands?
        {PREFIX}help - show this message
        {PREFIX}play <rock/paper/scissors> - play the game by making a choice
    """
    )

    await bot.api.send_text_message(room.room_id, message)
    
bot.add_message_listener(help_message)


async def make_choice(room, message):
    match = botlib.MessageMatch(room, message, bot)
    if not (
        match.not_from_this_bot() and match.prefix(PREFIX) and match.command("play")
    ):
        return
    
    args = match.args.split(' ')

    temp = True
    if "rock" in args:
        choice = "rock"
    elif "paper" in args:
        choice = "paper"
    elif "scissors" in args:
        choice = "scissors"
    else:
        temp = False
    
    victory_table = {
        "rock" : "scissors",
        "scissors" : "paper",
        "paper" : "rock"
    }
    
    if temp:
        bot_choice = random.choice(["rock", "paper", "scissors"])

        await bot.api.send_text_message(room.room_id, f"You choose {choice}.")
        await bot.api.send_text_message(room.room_id, f"The bot chose {bot_choice}.")

        if choice == bot_choice:
            await bot.api.send_text_message(room.room_id, "You Tied!")
        if bot_choice == victory_table[choice]:
            await bot.api.send_text_message(room.room_id, "You Won!")
        if choice == victory_table[bot_choice]:
            await bot.api.send_text_message(room.room_id, "You Lost!")
    
    else:
        await bot.api.send_text_message(room.room_id, "Invalid choice. Please choose \"rock\", \"paper\", or \"scissors\".")

bot.add_message_listener(make_choice)


bot.run()

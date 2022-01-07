"""
Example Usage:

random_user
      !echo something

random_user2
      *reacts with 👍️

echo_reaction_bot
      Reaction: 👍️
"""

import simplematrixbotlib as botlib

creds = botlib.Creds("https://example.com", "echo_reaction_bot", "password")
bot = botlib.Bot(creds)


@bot.listener.on_reaction_event
async def echo_reaction(room, event, reaction):
    resp_message = f"Reaction: {reaction}"
    await bot.api.send_text_message(room.room_id, resp_message)


bot.run()

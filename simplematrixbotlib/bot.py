import asyncio
import simplematrixbotlib as botlib

class Bot:
    """
    A class for the bot developer to primarily interact with
    Example Usage:

    import simplematrixbotlib as bl
    
    creds = bl.Creds("home.server", "user", "pass")
    bot = bl.Bot(creds)
    bot.run()
    """
    
    def __init__(self, creds):
        self.creds = creds
        self.api = botlib.API(self.creds)

    async def main(self):
        await self.api.login()
        while True:
            pass

    def run(self):
        asyncio.run(self.main())




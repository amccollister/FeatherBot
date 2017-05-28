import sqlite3 as sql
import random
import asyncio
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    bal = 100
    bot = None
    # TODO balance give lottery leaderboard slots flip blackjack?

    def __init__(self, bot):
        self.bot = bot
        asyncio.async(self.payout())

    @asyncio.coroutine
    async def payout(self):
        while True:
            self.bal += 10
            await asyncio.sleep(5)

    def cmd_moneyping(self, *_):
        return "$$$ pong"

    def cmd_balance(self, *_):
        return "You currently have __**{:,}**__ points.".format(self.bal)

    def cmd_give(self, *_):
        pass

    def cmd_lottery(self, *_):
        pass

    def cmd_leaderboard(self, *_):
        pass

    def cmd_slots(self, *_):
        pass

    def cmd_flip(self, _, *bet):  # flip 44k
        try:
            payout = int(bet[0][0])
            if payout <= 0:
                return "You can't bet nothing!"
            elif payout > self.bal:
                return "You don't have enough to bet!"
        except: return "You didn't place a bet!"
        call = random.choice(["heads", "tails"])
        land = random.choice(["heads", "tails"])
        result = "WIN"
        if call != land:
            payout *= -1
            result = "LOSE"
        self.bal += payout
        return "YOU {0}! You now have __**{1}**__ points.".format(result, format(self.bal, ",d"))


    def cmd_blackjack(self, *_): # ???
        pass

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
            print(self.bal)
            await asyncio.sleep(5)

    def cmd_moneyping(self, *_):
        return "$$$ pong"

    def cmd_balance(self, *_):
        return "You currently have {0} points.".format(self.bal)

    def cmd_give(self, *_):
        pass

    def cmd_lottery(self, *_):
        pass

    def cmd_leaderboard(self, *_):
        pass

    def cmd_slots(self, *_):
        pass

    def cmd_flip(self, _, *bet):
        try:    payout = int(bet[0][0])
        except Exception as e: return str(e) + " You didn't place a bet!"
        call = random.choice(["heads", "tails"])
        land = random.choice(["heads", "tails"])
        result = "WIN"
        if call != land:
            payout *= -1
            result = "LOSE"
        self.bal += payout
        return "YOU {0}! You now have {1} points.".format(result, self.bal)


    def cmd_blackjack(self, *_): # ???
        pass

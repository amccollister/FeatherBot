import sqlite3 as sql
import random
import asyncio
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    bal = 10000
    bot = None
    # TODO lottery slots blackjack?

    def __init__(self, client):
        self.con = sql.connect("db/currency.sqlite", isolation_level=None)
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS CURRENCY (ID INTEGER PRIMARY KEY, BALANCE INTEGER)")
        self.con.commit()
        self.bot = client
        self.add_users(self.bot.get_all_members())
        asyncio.async(self.payout())

    @asyncio.coroutine
    async def payout(self):  # SET TO ONLY PEOPLE ONLINE
        while True:
            await asyncio.sleep(10)
            self.c.execute("UPDATE CURRENCY SET BALANCE = BALANCE + 100")
            self.con.commit()

    def add_users(self, mem_list):
        for m in mem_list:
            self.c.execute("INSERT OR IGNORE INTO CURRENCY (ID, BALANCE) VALUES ({id}, 0)".format(id=m.id))
            self.con.commit()
        self.c.execute("SELECT * FROM CURRENCY")
        print(self.c.fetchall())

    def get_bal(self, user_id):
        self.c.execute("SELECT * FROM CURRENCY WHERE ID = {id}".format(id=user_id))
        return int(self.c.fetchone()[1])

    def update_bal(self, user_id, bal):
        self.c.execute("UPDATE CURRENCY SET BALANCE = BALANCE + {bal} WHERE ID = {id}".format(bal=bal, id=user_id))
        self.con.commit()

    def check_input(self, message, *args):
        bal = self.get_bal(message.author.id)
        try:
            input = int(args[0][0])
            if input <= 0:
                return "You can't offer nothing!"
            elif input > bal:
                return "You don't have enough to offer!"
        except:
            return "You didn't place an offer!"
        return input

    def cmd_moneyping(self, *_):
        return "$$$ pong"

    def cmd_bal(self, message, *_):
        return self.cmd_balance(message)

    def cmd_balance(self, message, *_):
        bal = self.get_bal(message.author.id)
        return "Hello, <@{0}>! You currently have __**{1}**__ points.".format(message.author.id, format(bal, ",d"))

    def cmd_buy(self, *_):
        pass

    def cmd_give(self, message, *args):
        try:
            user_id = int(args[0][1].lstrip("<!@").rstrip(">"))
        except:
            return "You gave nothing to no one. Charitable! (I could not find that user)"
        money = self.check_input(message, args[0])
        if type(money) is str:
            return money
        self.update_bal(user_id, money)
        self.update_bal(message.author.id, money * -1)
        return "<@{0}> gave __**{1}**__ points to <@{2}>".format(message.author.id, format(money, ",d"), user_id)

    def cmd_lottery(self, *_):
        pass

    def cmd_leaderboard(self, *_):
        self.c.execute("SELECT * FROM CURRENCY ORDER BY BALANCE DESC LIMIT 10")
        leaders = self.c.fetchall()
        output = "__**LEADERBOARD**__```"
        for l in leaders:
            member = list(self.bot.servers)[0].get_member(str(l[0]))
            name = member.nick
            if not name:  name = member.name
            output += "{0}\t\t{1}\n".format(name, format(l[1], ",d"))
        return output + "```"

    def cmd_slots(self, *_):
        pass

    def cmd_bet(self, message, *args):  # BET 44k BET ALL
        payout = self.check_input(message, args[0])
        if type(payout) is str:
            return payout
        call = random.choice(["heads", "tails"])
        land = random.choice(["heads", "tails"])
        result = "WON"
        if call != land:
            payout *= -1
            result = "LOST"
        self.update_bal(message.author.id, payout)
        return "<@{0}> {1}! You now have __**{2}**__ points.".format(message.author.id, result,
                                                                     format(self.get_bal(message.author.id), ",d"))

    def cmd_blackjack(self, *_):  # ???
        pass

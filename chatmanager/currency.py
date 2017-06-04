import sqlite3 as sql
import random
import asyncio
import constants

from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = bot = None  # Defining connection and cursor for sql DB
    lottery = []
    server = None
    #TODO SET TO ONLY PEOPLE ONLINE AND LOTTO EVERY 10 MINS w/ COUNTDOWN

    def __init__(self, client):
        self.con = sql.connect("db/currency.sqlite", isolation_level=None)
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS CURRENCY (ID INTEGER PRIMARY KEY, BALANCE INTEGER)")
        self.con.commit()
        self.bot = client
        self.add_users(self.bot.get_all_members())
        asyncio.async(self.payout())

    @asyncio.coroutine
    async def payout(self):
        while True:
            await asyncio.sleep(60)
            self.c.execute("UPDATE CURRENCY SET BALANCE = BALANCE + 10")
            self.con.commit()
            await self.bot.send_message(self.bot.get_channel("312852004999266304"), self.draw_lottery())

    def draw_lottery(self):
        if not self.lottery:
            return "__**LOTTERY**__\nNobody bought any tickets."
        user_id = random.choice(self.lottery)
        payout = len(self.lottery) * constants.LOTTERY_PRICE
        tickets = 0
        for ticket in self.lottery:
            if ticket == user_id:
                tickets += 1
        self.lottery = []
        self.update_bal(user_id, payout)
        return "__**LOTTERY**__\nCONGRATULATIONS to <@{0}> on winning __**{1}**__ " \
               "points with {2} tickets.".format(user_id, format(payout, ",d"), tickets)

    def add_users(self, mem_list):
        for m in mem_list:
            self.c.execute("INSERT OR IGNORE INTO CURRENCY (ID, BALANCE) VALUES ({id}, 0)".format(id=m.id))
            self.con.commit()
        self.c.execute("SELECT * FROM CURRENCY")
        #print(self.c.fetchall())

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

    def cmd_buy(self, message, *args):
        tickets = self.check_input(message, args[0])
        if type(tickets) is str:  return tickets
        cost = tickets * constants.LOTTERY_PRICE
        if cost > self.get_bal(message.author.id): return "You can't afford that many tickets!"
        for i in range(tickets):
            self.lottery.append(message.author.id)
        self.update_bal(message.author.id, cost * -1)
        return "__**LOTTERY**__\n<@{0}> just purchased {1} tickets!".format(message.author.id, tickets)

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
        return "<@{0}> gave __**{1}**__ points to <@{2}>".format(message.author.id, format(money, ",.0f"), user_id)

    def cmd_lottery(self, *_):
        return "__**LOTTERY**__\nThe jackpot sits at __**{:,d}**__ points.".format(len(self.lottery)*constants.LOTTERY_PRICE)

    def cmd_leaderboard(self, *_):
        self.c.execute("SELECT * FROM CURRENCY ORDER BY BALANCE DESC LIMIT 10")
        leaders = self.c.fetchall()
        output = "__**LEADERBOARD**__```"
        for l in leaders:
            member = list(self.bot.servers)[0].get_member(str(l[0]))
            name = member.nick
            if not name:  name = member.name
            output += "{0}\t\t{1}\n".format(name, format(l[1], ",.0f"))
        return output + "```"

    def cmd_slots(self, message, *args):
        bet = self.check_input(message, args[0])
        if type(bet) is str:
            return bet
        wheel = [":white_check_mark:", ":seven:", ":bell:", ":no_entry_sign:",
                 ":large_blue_diamond:", ":moneybag:", ":triangular_flag_on_post:"]
        w1 = random.randrange(0, 6); w2 = random.randrange(0, 6); w3 = random.randrange(0, 6)
        spin = [[w1, w2, w3], [(w1+1)%7, (w2+1)%7, (w3+1)%7], [(w1+2)%7, (w2+2)%7, (w3+2)%7]]
        output = "| "
        win = self.get_payout(spin[1], bet)
        self.update_bal(message.author.id, win)
        for w in spin:
            for i in range(3):
                output += wheel[w[i]] + " | "
                if w[0] == spin[1][0] and i == 2:
                    output += "  <@{0}>'s Payout:  __**{1}**__".format(message.author.id, format(int(win+bet), ",d"))
            output += "\n| "
        return output[:-3]

    def get_payout(self, wheel, bet):
        payout = [10, 77, 11, 0, 15, 20, 5]
        winnings = bet
        if wheel[0] == wheel[1] and wheel[1] == wheel[2]:
            winnings *= payout[wheel[1]]
        elif wheel[0] == wheel[1] or wheel[1] == wheel[2]:
            winnings *= (payout[wheel[1]] * 0.1)
        else:
            return winnings * -1
        winnings -= bet
        return winnings

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

import sqlite3 as sql
import random
import asyncio
import constants

from datetime import timedelta
from datetime import datetime
from chatmanager import bot

#TODO horse race?


class Plugin(bot.ChatManager):
    def __init__(self, client):
        self.con = sql.connect("db/currency.sqlite", isolation_level=None)
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS CURRENCY (ID INTEGER PRIMARY KEY, BALANCE INTEGER)")
        self.con.commit()
        self.bot = client
        self.lottery = []
        self.next_draw = datetime.now() + timedelta(seconds=constants.DRAW_TIME)
        asyncio.async(self.payout())
        asyncio.async(self.lottery_draw())

    @asyncio.coroutine
    async def payout(self):
        while True:
            await asyncio.sleep(constants.PAY_TIME)
            self.add_users(self.bot.get_all_members())
            online_users = []
            for u in self.bot.get_all_members():
                if str(u.status) != "offline":
                    online_users.append([constants.PAYCHECK, u.id])
            self.c.execute("BEGIN TRANSACTION")
            self.c.executemany("UPDATE CURRENCY SET BALANCE = BALANCE + ? WHERE ID = ?", online_users)
            self.c.execute("COMMIT")
            self.con.commit()

    @asyncio.coroutine
    async def lottery_draw(self):
        while True:
            await asyncio.sleep(constants.DRAW_TIME)
            self.next_draw = datetime.now() + timedelta(seconds=constants.DRAW_TIME)
            await self.bot.send_message(self.bot.get_channel(constants.LOTTERY_CHANNEL), self.draw_lottery())

    def draw_lottery(self):
        if not self.lottery:
            return "__**LOTTERY**__\nNobody bought any tickets."
        user_id = random.choice(self.lottery)
        payout = int(len(self.lottery) * constants.LOTTERY_PRICE * .9)
        tickets = 0
        total = len(self.lottery)
        for ticket in self.lottery:
            if ticket == user_id:
                tickets += 1
        self.lottery = []
        self.update_bal(user_id, payout)
        return "__**LOTTERY**__\nCONGRATULATIONS to <@{0}> on winning __**{1}**__ " \
               "points with {2} tickets.\n The pot held {3} tickets!".format(user_id, format(payout, ",d"), tickets, total)

    def add_users(self, mem_list):
        id_list = []
        for m in mem_list:
            id_list.append([m.id, 0])
        self.c.execute("BEGIN TRANSACTION")
        self.c.executemany("INSERT OR IGNORE INTO CURRENCY ('ID', 'BALANCE') VALUES(?, ?)", id_list)
        self.c.execute("COMMIT")
        self.con.commit()

    def get_bal(self, user_id):
        self.c.execute("SELECT * FROM CURRENCY WHERE ID = {id}".format(id=user_id))
        self.con.commit()
        return int(self.c.fetchone()[1])

    @staticmethod
    def get_role(message, role_id):
        for r in message.server.roles:
            if r.id == role_id:
                return r
        return None

    def update_bal(self, user_id, bal):
        self.c.execute("UPDATE CURRENCY SET BALANCE = BALANCE + {bal} WHERE ID = {id}".format(bal=bal, id=user_id))
        self.con.commit()

    def check_input(self, message, *args):
        bal = self.get_bal(message.author.id)
        short_hand = {"k": 10**3, "m": 10**6, "b": 10**9, "t": 10**12, "q": 10**15}
        try:
            arg = args[0][0]
            if arg.lower() == "all": return bal
            if arg[-1:].lower() in ["k", "m", "b", "t", "q"]:
                input = int(arg[:-1])
                suffix = arg[-1:].lower()
                input *= short_hand[suffix]
            else:
                input = int(arg)
            if input <= 0:
                return "You can't offer nothing!"
            elif input > bal:
                return "You don't have enough to offer!"
        except:
            return "You didn't place an offer!"
        return input

    async def cmd_bal(self, message, *_):
        """
        Usage:
                !bal

        Displays your balance.
        """
        await self.cmd_balance(message)

    async def cmd_balance(self, message, *_):
        """
        Usage:
                !balance

        Displays your balance.
        """
        bal = self.get_bal(message.author.id)
        await self.bot.send_msg(message.channel, "Hello, <@{0}>! You currently have __**{1}**__ points.".format(message.author.id, format(bal, ",d")))

    async def cmd_buy(self, message, *args):
        """
        Usage:
                !buy <tickets>

        Purchases a specified number of tickets for the next lottery.
        """
        tickets = self.check_input(message, args[0])
        if type(tickets) is str:  await self.bot.send_msg(message.channel,  tickets)
        cost = tickets * constants.LOTTERY_PRICE
        if cost > self.get_bal(message.author.id): await self.bot.send_msg(message.channel, "You can't afford that many tickets!")
        for i in range(tickets):
            self.lottery.append(message.author.id)
        self.update_bal(message.author.id, cost * -1)
        await self.bot.send_msg(message.channel, "__**LOTTERY**__\n<@{0}> just purchased {1} tickets!".format(message.author.id, tickets))

    async def cmd_give(self, message, *args):
        """
        Usage:
                !give <amount> <@user> 

        Gives a user some points from your balance.
        Consider it a gift and don't expect to get it back.
        """
        try:
            user_id = int(args[0][1].lstrip("<!@").rstrip(">"))
        except:
            await self.bot.send_msg(message.channel, "You gave nothing to no one. Charitable! (I could not find that user)")
        money = self.check_input(message, args[0])
        if type(money) is str:
            await self.bot.send_msg(message.channel, money)
        self.update_bal(user_id, money)
        self.update_bal(message.author.id, money * -1)
        await self.bot.send_msg(message.channel, "<@{0}> gave __**{1}**__ points to <@{2}>".format(message.author.id, format(money, ",.0f"), user_id))

    async def cmd_lottery(self, message, *_):
        """
        Usage:
                !lottery

        Displays the jackpot and time until next draw.
        """
        time = self.next_draw - datetime.now()
        minutes = int(time.total_seconds()/60)
        seconds = int(time.total_seconds()%60)
        time_remaining = "{0}min {1}sec".format(minutes, seconds)
        await self.bot.send_msg(message.channel, "__**LOTTERY**__\nThe jackpot sits at __**{:,d}**__ points.\n" \
               "Draw in {}!".format(int(len(self.lottery)*constants.LOTTERY_PRICE*.9), time_remaining))

    async def cmd_leaderboard(self, message, *_):
        """
        Usage:
                !leaderboard

        Displays the 10 users with the highest balance on the server.
        """
        self.c.execute("SELECT * FROM CURRENCY ORDER BY BALANCE DESC LIMIT 10")
        leaders = self.c.fetchall()
        output = "__**LEADERBOARD**__```"
        for l in leaders:
            member = message.server.get_member(str(l[0]))
            if not member: continue # TODO if a user leaves, they're still in db... clean this up
            name = member.nick
            if not name:  name = member.name
            output += "{:12s}\t\t{:,.0f}\n".format(name[:12], l[1]) #format(, ",.0f"))
        await self.bot.send_msg(message.channel, output + "```")

    async def cmd_slots(self, message, *args):
        """
        Usage:
                !slots <amount>

        Insert some money into the slot machine and give it a spin.
        """
        pay = self.check_input(message, args[0])
        if type(pay) is str:
            return await self.bot.send_msg(message.channel, pay)
        wheel = [":white_check_mark:", ":seven:", ":bell:", ":no_entry_sign:",
                 ":large_blue_diamond:", ":moneybag:", ":triangular_flag_on_post:"]
        w1 = random.randrange(0, 6); w2 = random.randrange(0, 6); w3 = random.randrange(0, 6)
        spin = [[w1, w2, w3], [(w1+1)%7, (w2+1)%7, (w3+1)%7], [(w1+2)%7, (w2+2)%7, (w3+2)%7]]
        output = "| "
        win = self.get_payout(spin[1], pay)
        self.update_bal(message.author.id, win)
        for w in spin:
            for i in range(3):
                output += wheel[w[i]] + " | "
                if w[0] == spin[1][0] and i == 2:
                    output += "  <@{0}>'s Payout:  __**{1}**__".format(message.author.id, format(win+pay, ",.0f"))
            output += "\n| "
        await self.bot.send_msg(message.channel, output[:-3])

    def get_payout(self, wheel, bet):
        pay = constants.SLOTS_PAYOUT
        winnings = bet
        if wheel[0] == wheel[1] and wheel[1] == wheel[2]:
            winnings *= int(pay[wheel[1]])
        elif wheel[0] == wheel[1] or wheel[1] == wheel[2]:
            winnings *= (float(pay[wheel[1]]) * 0.1)
        else:
            return winnings * -1
        print(winnings, bet, wheel)
        winnings -= bet
        return winnings

    async def cmd_bet(self, message, *args):  # BET 44k BET ALL
        """
        Usage:
                !bet [ALL | 1K/1M/1B/1T | <number>]

        Bets a certain amount of money on a coin toss. Double or nothing!
        You may input a number, ALL, or K, M, B, T behind a number.
        K = thousand M = million B = billion T = trillion
        Be careful when betting ALL. You may lose everything. No take backs!
        """
        pay = self.check_input(message, args[0])
        if type(pay) is str:
            return await self.bot.send_msg(message.channel, pay)
        call = random.choice(["heads", "tails"])
        land = random.choice(["heads", "tails"])
        result = "WON"
        if call != land:
            pay *= -1
            result = "LOST"
        self.update_bal(message.author.id, pay)
        await self.bot.send_msg(message.channel, "<@{0}> {1}! You now have __**{2}**__ points.".format(message.author.id, result, format(self.get_bal(message.author.id), ",d")))

    async def cmd_rankup(self, message, *args):
        """
        Usage:
                !rankup [l | list]

        Ranks you up to the next highest tier.
        Use !rankup list or !rankup l to display all the ranks and their costs.
        """
        role = message.author.top_role
        arg = args and args[0] or None
        error = "There's a problem with the rankup list.\n The feature is currently disabled. Please contact the owner."
        if len(constants.RANK_COST) != len(constants.RANK_LIST):
            return await self.bot.send_msg (message.channel, error)
        elif role.id == constants.RANK_LIST[-1:][0]:
            return await self.bot.send_msg(message.channel, "You're already the highest rank.")
        try:
            if arg is None:
                index = 0
                for i in range(len(constants.RANK_LIST)-1):
                    if role.id == constants.RANK_LIST[i]:
                        index = i+1
                        break
                r = self.get_role(message, constants.RANK_LIST[index])
                if self.get_bal(message.author.id) < int(constants.RANK_COST[index]): return await self.bot.send_msg(message.channel, "You cannot afford to rank up, yet!")
                self.update_bal(message.author.id, -int(constants.RANK_COST[index]))
                await self.bot.add_roles(message.author, r)
                await self.bot.send_msg(message.channel, "Congratulations! You are now part of the {} rank!\nYou now have **{}** points.".format(r, format(self.get_bal(message.author.id), ",d")))
            else:
                output = "__**RANK LIST**__```"
                for i in range(len(constants.RANK_LIST)):
                    output += "{:15s}{:,.0f}\n".format(str(self.get_role(message, constants.RANK_LIST[i])), int(constants.RANK_COST[i]))
                output += "```"
                await self.bot.send_msg(message.channel, output)
        except:
            await self.bot.send_msg(message.channel, error)

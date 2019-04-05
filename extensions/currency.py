import sqlite3 as sql
import random
import constants
import discord
import operator
from datetime import datetime

import json
import html
import urllib.request
import urllib.error

from discord.ext import commands
import extensions.utils as util


class CurrencyCog:
    def __init__(self, bot):
        self.con = sql.connect("db/database.db", isolation_level=None)
        self.cur = self.con.cursor()
        with open('db/schema.sql') as schema:
            self.cur.executescript(schema.read())
        self.add_users(bot.get_all_members())
        self.con.commit()

    def add_users(self, mem_list):
        id_list = []
        for m in mem_list:
            id_list.append([m.id, m.name, 0])
        self.cur.execute("BEGIN TRANSACTION")
        self.cur.executemany("INSERT OR IGNORE INTO CURRENCY ('ID', 'NAME', 'BALANCE') VALUES(?, ?, ?)", id_list)
        self.cur.execute("COMMIT")
        self.con.commit()

    def get_bal(self, user_id):
        self.cur.execute("SELECT * FROM CURRENCY WHERE ID = {id}".format(id=user_id))
        self.con.commit()
        return self.cur.fetchone()[2]

    def update_bal(self, uid, amt):
        self.cur.execute("UPDATE CURRENCY SET BALANCE = BALANCE + {amt} WHERE ID = {uid}".format(amt=amt, uid=uid))
        self.con.commit()

    def get_price(self, crypto):
        link = "https://api.cryptonator.com/api/ticker/{}-usd".format(crypto)
        with urllib.request.urlopen(link) as response:
            payload = json.loads(response.read())
        price = -1
        if payload["success"]:
            price = float(payload["ticker"]["price"]) * 100
        return int(price)

    def buy_crypto(self, user, amt, coin, total):
        self.cur.execute("SELECT * FROM CRYPTO WHERE ID = {uid} AND COIN = \"{coin}\"".format(uid=user.id, coin=coin))
        wallet = self.cur.fetchall()
        if self.get_bal(user.id) < total:
            return "insufficient funds"
        if wallet:
            self.cur.execute("UPDATE CRYPTO SET AMOUNT=AMOUNT+{amt} WHERE ID={uid} and COIN=\"{coin}\""
                             .format(amt=amt, coin=coin, uid=user.id))
        else:
            self.cur.execute("INSERT INTO CRYPTO VALUES({}, \"{}\", {}, \"{}\")".format(user.id, user, amt, coin))
        self.update_bal(user.id, total*-1)
        self.con.commit()
        return True

    def sell_crypto(self, user, amt, coin, total):
        self.cur.execute("SELECT * FROM CRYPTO WHERE ID = {uid} AND COIN = \"{coin}\"".format(uid=user.id, coin=coin))
        wallet = self.cur.fetchone()
        if not wallet or wallet[2] < amt:
            return "insufficient coin balance"
        self.update_bal(user.id, total)
        if wallet[2] == amt:
            self.cur.execute("DELETE FROM CRYPTO WHERE ID={uid} and COIN=\"{coin}\"".format(coin=coin, uid=user.id))
        else:
            self.cur.execute("UPDATE CRYPTO SET AMOUNT=AMOUNT-{amt} WHERE ID={uid} and COIN=\"{coin}\""
                             .format(amt=amt, coin=coin, uid=user.id))
        self.con.commit()
        return True

    @commands.command(aliases=["bal", "points", "pts"])
    async def balance(self, ctx):
        """
        Usage:
                !balance

        Displays your current points total.
        """
        bal = format(self.get_bal(ctx.author.id), ",d")
        text = "__Your Wallet__\n**{}** points\n".format(bal)
        self.cur.execute("SELECT * FROM CRYPTO WHERE ID = {}".format(ctx.author.id))
        coins = self.cur.fetchall()
        for c in coins:
            text += "**{0}** {1}\n".format(c[2], c[3])
        await util.send(ctx, text)

    def check_input(self, ctx, arg):
        bal = self.get_bal(ctx.author.id)
        short_hand = {"k": 10**3, "m": 10**6, "b": 10**9, "t": 10**12, "q": 10**15}
        try:
            if bal <= 0: return "You have nothing to offer...\nCome back when you get some dough."
            elif arg.lower() == "all": return bal
            elif arg[-1:].lower() in ["k", "m", "b", "t", "q"]:
                output = int(arg[:-1])
                suffix = arg[-1:].lower()
                output *= short_hand[suffix]
            else:
                output = int(arg)
            if output <= 0:
                return "You can't offer nothing!"
            elif output > bal:
                return "You don't have enough to offer!"
        except:
            return "You didn't place a valid offer!"
        return output

    @commands.command()
    async def give(self, ctx, user, amount):
        """
        Usage:
                !give [@user] [points]

        Generously donates some of your points to another user.
        """
        try:
            u = await commands.UserConverter().convert(ctx, user)
            a = self.check_input(ctx, amount)
        except commands.errors.BadArgument:
            return await util.send(ctx, "**ERROR**\nI could not find this user.")
        except ValueError:
            return await util.send(ctx, "**ERROR**\nThat is an inappropriate amount.")
        text = "You gave **{0}** points to {1}".format(format(a, ",d"), u.mention)
        print(ctx.author.id, u.id)
        self.update_bal(ctx.author.id, a*-1)
        self.update_bal(u.id, a)
        await util.send(ctx, text)

    @commands.command()
    async def leaderboard(self, ctx):
        """
        Usage:
                !leaderboard

        Shows the top 10 earners on the server.
        """
        self.cur.execute("SELECT * FROM CURRENCY ORDER BY BALANCE DESC LIMIT 10")
        leaders = self.cur.fetchall()
        embed = discord.Embed()
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="FeatherBot v0.0.1")
        embed.add_field(name="leaderboard", value="top 10", inline=False)
        for i, l in enumerate(leaders):
            name = l[1]; bal = l[2]
            embed.add_field(name="{0}. {1}".format(i+1, name), value=format(bal, ",d"), inline=False)
        await util.send_embed(ctx, embed)

    @commands.command()
    async def slots(self, ctx, amt):
        """
        Usage:
                !slots [bet]

        Spins the slot machine with your bet. Warning: you have a high chance to lose!
        """
        arg = self.check_input(ctx, amt)
        if type(arg) is str:
            return await util.send(ctx, arg)
        self.update_bal(ctx.author.id, arg*-1)
        wheel = [":no_entry_sign:", ":triangular_flag_on_post:", ":bell:", ":moneybag:",
                 ":white_check_mark:", ":large_blue_diamond:", ":seven:"]
        w1 = random.randrange(0, 6)
        w2 = random.randrange(0, 6)
        w3 = random.randrange(0, 6)
        win = 0
        if w1 == w2 and w2 == w3:
            win = 5 * w1
        elif w1 == w2 or w2 == w3:
            win = random.choice([w1, w2, w3])
        payout = arg * win
        spin = [[w1, w2, w3],
                [(w1 + 1) % 7, (w2 + 1) % 7, (w3 + 1) % 7],
                [(w1 + 2) % 7, (w2 + 2) % 7, (w3 + 2) % 7]]
        text = ""
        self.update_bal(ctx.author.id, payout)
        for w in spin:
            text += "\n| "
            for i in range(3):
                text += wheel[w[i]] + " | "
        text += "\nYou received **{0}** points.".format(format(payout, ",d"))
        await util.send(ctx, text)

    @commands.command()
    async def bet(self, ctx, amt):
        """
        Usage:
                !bet [points]

        Flips a coin. If it's tails, you win double your money!
        """
        arg = self.check_input(ctx, amt)
        if type(arg) is str:
            return await util.send(ctx, arg)
        land = random.choice([0, 1])
        result = "WON"
        if land == 0:
            arg *= -1
            result = "LOST"
        self.update_bal(ctx.author.id, arg)
        new_bal = self.get_bal(ctx.author.id)
        text = "**YOU {0}!**\nYou now have **{1}** points!".format(result, format(new_bal, ",d"))
        await util.send(ctx, text)

    @commands.command()
    async def math(self, ctx):
        """
        Usage:
                !math

        Gives you a random math question to solve.
        You only have 6 seconds to answer so be fast!
        """
        ops = {"plus": operator.add,
               "minus": operator.sub,
               "times": operator.mul,
               "divided by": operator.floordiv,
               "modulus": operator.mod}
        a = random.randint(0, 32)
        b = random.randint(1, 32)
        op = random.choice(list(ops.keys()))
        if op in ["plus", "minus"]: mult = .25
        elif op in ["divided by", "modulus"]: mult = 1
        else: mult = 1 + ((a+b)/100)
        mult += (a+b)/1000
        payout = [-1 * int((2-mult)*constants.PAYCHECK), int(mult*constants.PAYCHECK)]  # 0 is wrong. 1 is correct.
        ans = ops.get(op)(a, b)
        correct = False
        await util.send(ctx, "What is **{0} {1} {2}**?".format(a, op, b))
        try:
            answer = await ctx.bot.wait_for("message",
                                            check=lambda x: x.channel == ctx.channel and x.author.id == ctx.author.id,
                                            timeout=6.0)
            now = datetime.now()
            if answer.content == str(ans):
                text = "That is correct!\nYou earned **{0}** points!".format(payout[1])
                correct = True
            else:
                text = "Incorrect!\nThe answer was **{0}**.".format(ans)
        except:
            text = "You took too long!\nThe answer was **{0}**.".format(ans)
        if correct: self.update_bal(ctx.author.id, payout[1])
        else:       self.update_bal(ctx.author.id, payout[0]); text += "\nYou lost **{0}** points!".format(payout[0])
        await util.send(ctx, text)

    @commands.command()
    async def trivia(self, ctx):
        link = "https://opentdb.com/api.php?amount=1&type=multiple"
        payout = {"easy": 2000, "medium": 4000, "hard": 6000}
        with urllib.request.urlopen(link) as response:
            payload = json.loads(response.read().decode())["results"][0]
        ans = [html.unescape(x) for x in payload["incorrect_answers"] + [payload["correct_answer"]]]
        output = [payload["category"], payload["difficulty"], html.unescape(payload["question"]), random.shuffle(ans)]
        loss = payout[payload["difficulty"]]/-20
        text = "**Category:** {0}\n**Difficulty:** {1}\n**Question:** {2}\n\n__**Choose One**__".format(*output)
        for i in range(4):
            if ans[i] == html.unescape(payload["correct_answer"]):
                letter = chr(i+65)
            text += "\n{}: {}".format(chr(i+65), ans[i])
        await util.send(ctx, text)
        try:
            start = datetime.now()
            answer = await ctx.bot.wait_for("message",
                                            check=lambda x: x.channel == ctx.channel and x.author.id == ctx.author.id,
                                            timeout=20.0)
            if answer.content == letter:
                end = datetime.now() - start
                time = end.seconds + end.microseconds/10**6
                time = .5 if time < .5 else time
                pay = int(payout[payload["difficulty"]]/time)
                self.update_bal(ctx.author.id, pay)
                response = "Correct! You took **{0}** seconds and earned a total of **{1}** points!".format(time, pay)
            else:
                self.update_bal(ctx.author.id, loss)
                response = "Incorrect! It was **{0}**. You lost **{1}** points.".format(letter, int(loss)*-1)
        except:
            response = "You took too long!\nThe answer was **{0}**. You lost **{1}** points".format(letter, int(loss)*-1)
            self.update_bal(ctx.author.id, loss)
        await util.send(ctx, response)

    @commands.command()
    async def crypto(self, ctx, *args):
        currencies = args or ["BTC", "ETH", "XRP", "EOS", "LTC"]
        if len(currencies) > 5:
            await util.send(ctx, "Please use less than 5 currencies in one list.")
            return None

        output = ""
        for c in currencies:
            price = self.get_price(c)
            output += "**{0}** \\|\\| {1} points\n".format(c, int(price))
        await util.send(ctx, output)

    @commands.command()
    async def buy(self, ctx, amt, coin):
        coin = coin.upper()
        try:
            amount = float(amt)
            if amount < 0:
                raise
        except:
            return await util.send(ctx, "Invalid amount!")
        price = self.get_price(coin)
        total = int(price * float(amt))
        result = self.buy_crypto(ctx.author, amt, coin, total)
        if type(result) == str:
            await util.send(ctx, "Transaction failed due to **{}**. Please try again.".format(result))
        else:
            await util.send(ctx, "Purchased {} units of {} for {} points".format(amt, coin, total))

    @commands.command()
    async def sell(self, ctx, amt, coin):
        coin = coin.upper()
        try:
            amount = float(amt)
            if amount < 0:
                raise
        except:
            return await util.send(ctx, "Invalid amount!")
        price = self.get_price(coin)
        total = int(price * float(amt))
        result = self.sell_crypto(ctx.author, amount, coin, total)
        if type(result) == str:
            await util.send(ctx, "Transaction failed due to **{}**. Please try again.".format(result))
        else:
            await util.send(ctx, "Sold {} units of {} for {} points".format(amt, coin, total))


def setup(bot):
    bot.add_cog(CurrencyCog(bot))

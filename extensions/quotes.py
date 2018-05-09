import sqlite3 as sql
import random

from datetime import datetime
from discord.ext import commands


class QuotesCog:
    #addquote quote undoquote redoquote removequote
    @commands.command()
    async def addquote(self, ctx):
        pass

    @commands.command()
    async def quote(self, ctx):
        pass

    @commands.command()
    async def undoquote(self, ctx):
        pass

    @commands.command()
    async def redoquote(self, ctx):
        pass

    @commands.command()
    async def removequote(self, ctx):
        pass


def setup(bot):
    bot.add_cog(QuotesCog())


'''
class Plugin(bot.ChatManager):
    def __init__(self, bot, *_):
        self.con = sql.connect("db/quotes.sqlite", isolation_level=None)
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS QUOTES (NAME TEXT, QUOTE TEXT, DATE TEXT)")
        self.con.commit()
        self.bot = bot
        self.undone_quote = None

    @staticmethod
    def print_quote(quote):
        date = ""
        if quote is None:
            return "I couldn't find any stored quotes!"
        if quote[3]:
            date = datetime.strptime(quote[3], "%Y-%m-%d").strftime("%B %d, %Y")
            date = " on " + date
        return "Quote #{0}: \"{1}\" by {2}".format(quote[0], quote[2], quote[1]) + date

    def get_quote(self, qnum):
        self.c.execute("SELECT ROWID, * FROM QUOTES WHERE ROWID = {id}".format(id=qnum))
        return self.c.fetchone()

    def remove_quote(self, qnum):
        del_quote = self.get_quote(qnum)
        self.c.execute("DELETE FROM QUOTES WHERE ROWID = {id};".format(id=qnum))
        self.c.execute("VACUUM")
        self.con.commit()
        return del_quote

    async def cmd_addquote(self, message, *args):
        """
        Usage:
                !addquote <name> <quote> [date]

        Adds a quote to the database for future reminiscence. 
        Requires the name and quote in order to be stored. 
        The date may be added using the following format: YYYY-MM-DD
        """
        if not args[0]:
            await self.bot.send_msg(message.channel, "You didn't add a quote.")
        name = args[0].pop(0)
        date = args[0].pop()
        quote = " ".join(args[0])
        try:
            datetime.strptime(date, "%Y-%m-%d")  # try to parse the date out. else not date
        except:
            quote = (quote + " " + date).strip()
            date = ""
        quote = quote.replace("'", "''")  # Single quote escape
        self.c.execute("INSERT INTO QUOTES(QUOTE, NAME, DATE) VALUES('{q}', '{n}', '{d}')".format(q=quote, n=name, d=date))
        self.c.execute("SELECT last_insert_rowid();")
        id = self.c.fetchone()[0]
        self.con.commit()
        await self.bot.send_msg(message.channel, "{0} **added** Quote #{1} to remember when {2} said \"{3}\"".format(self.get_name(message),  # hide '' from user
                                                                               id, name, quote.replace("''", "'")))

    async def cmd_quote(self, message, *args): # fix detecting empty db
        """
        Usage:
                !quote [id]

        Grabs a quote from the database with the specified ID.
        If no ID is provided, a random quote will be displayed.
        """
        if not args[0]:
            self.c.execute("SELECT ROWID, * FROM QUOTES")
            quote = random.choice(self.c.fetchall())
        else:
            try:
                quote = self.get_quote(args[0][0])
                if not quote: raise Exception
            except:
                await self.bot.send_msg(message.channel, "I could not find a quote with that ID.")
        await self.bot.send_msg(message.channel, self.print_quote(quote))

    async def cmd_undoquote(self, message, *args):
        """
        Usage:
                !undoquote

        Removes the latest quote added for when someone makes a typo.
        """
        self.c.execute("SELECT last_insert_rowid();")
        id = self.c.fetchone()[0]
        try:
            if id == 0: raise Exception
            self.undone_quote = self.remove_quote(id)
            await self.bot.send_msg(message.channel, "{0} **removed** {1}".format(self.get_name(message), self.print_quote(self.undone_quote)))
        except:
            await self.bot.send_msg(message.channel, "There's no quote to undo!")

    async def cmd_redoquote(self, message, *_):
        """
        Usage:
                !redoquote

        Adds the latest quote that was deleted. 
        Useful for when you want to undo the undo or accidentally delete the wrong ID.
        """
        if self.undone_quote is None:
            await self.bot.send_msg(message.channel, "No quotes have been undone recently.")
        else:
            quote = " ".join(self.undone_quote[1:]).rstrip(" ").split(" ")  # Remove spaces if no date in quote
            await self.cmd_addquote(message, quote)
        pass

    async def cmd_removequote(self, message, *args):
        """
        Usage:
                !removequote <id>

        Removes the quote with the specified ID.
        If no ID is specified, no quotes will be deleted because deleting random quotes would be silly.
        """
        try:
            del_quote = self.remove_quote(int(args[0][0]))
            if not del_quote: raise Exception
            await self.bot.send_msg(message.channel, "{0} **removed** {1}".format(self.get_name(message), self.print_quote(del_quote)))
        except:
            await self.bot.send_msg(message.channel, "I could not find a quote with that ID.")
'''
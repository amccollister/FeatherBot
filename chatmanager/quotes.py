import sqlite3 as sql
import random

from datetime import datetime
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    #TODO redoquote

    def __init__(self, bot, *_):
        self.con = sql.connect("db/quotes.sqlite", isolation_level=None)
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS QUOTES (NAME TEXT, QUOTE TEXT, DATE TEXT)")
        self.con.commit()
        self.bot = bot

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
                !command [params]

        This describes what the command does.
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
                !command [params]

        This describes what the command does.
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
                !command [params]

        This describes what the command does.
        """
        self.c.execute("SELECT last_insert_rowid();")
        id = self.c.fetchone()[0]
        try:
            del_quote = self.remove_quote(id)
            await self.bot.send_msg(message.channel, "{0} **removed** {1}".format(self.get_name(message), self.print_quote(del_quote)))
        except:
            await self.bot.send_msg(message.channel, "There's no quote to undo!")

    async def cmd_removequote(self, message, *args):
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        try:
            del_quote = self.remove_quote(int(args[0][0]))
            if not del_quote: raise Exception
            await self.bot.send_msg(message.channel, "{0} **removed** {1}".format(self.get_name(message), self.print_quote(del_quote)))
        except:
            await self.bot.send_msg(message.channel, "I could not find a quote with that ID.")

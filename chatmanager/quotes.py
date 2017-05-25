import sqlite3 as sql
import random
from datetime import datetime
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB

    def __init__(self):
        self.con = sql.connect("db/quotes.sqlite", isolation_level=None)
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS QUOTES (NAME TEXT, QUOTE TEXT, DATE TEXT)")
        self.con.commit()

    def get_quote(self, qnum):
        self.c.execute("SELECT ROWID, * FROM QUOTES WHERE ROWID = {id}".format(id=qnum))
        return self.c.fetchone()

    def remove_quote(self, qnum):
        del_quote = self.get_quote(qnum)
        self.c.execute("DELETE FROM QUOTES WHERE ROWID = {id};".format(id=qnum))
        self.c.execute("VACUUM")
        self.con.commit()
        return del_quote

    def print_quote(self, quote):
        date = ""
        if quote[3]:
            date = datetime.strptime(quote[3], "%Y-%m-%d").strftime("%B %d, %Y")
            date = " on " + date
        return "Quote #{0}: \"{1}\" by {2}".format(quote[0], quote[2], quote[1]) + date

    def cmd_addquote(self, message, *args):
        if not args[0]:
            return "You didn't add a quote."
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
        return "{0} **added** Quote #{1} to remember when {2} said \"{3}\"".format(message.author.name,  # hide '' from user
                                                                               id, name, quote.replace("''", "'"))

    def cmd_quote(self, message, *args):
        if not args[0]:
            self.c.execute("SELECT ROWID, * FROM QUOTES")
            quote = random.choice(self.c.fetchall())
        else:
            try:
                #self.c.execute("SELECT ROWID, * FROM QUOTES WHERE ROWID = {id}".format(id=int(args[0][0])))
                quote = self.get_quote(args[0][0])
                if not quote: raise
            except:
                return "I could not find a quote with that ID."
        return self.print_quote(quote)

    def cmd_undoquote(self, message, *args):
        self.c.execute("SELECT last_insert_rowid();")
        id = self.c.fetchone()[0]
        try:
            del_quote = self.remove_quote(id)
            return "{0} **removed** {1}".format(message.author.name, self.print_quote(del_quote))
        except:
            return "There's no quote to undo!"

    def cmd_removequote(self, message, *args):
        try:
            del_quote = self.remove_quote(int(args[0][0]))
            if not del_quote: raise
            return "{0} **removed** {1}".format(message.author.name, self.print_quote(del_quote))
        except Exception as e:
            return "I could not find a quote with that ID."

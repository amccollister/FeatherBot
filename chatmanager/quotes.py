import sqlite3 as sql
import random
from datetime import datetime
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    # TODO: removequote undoquote updatequote

    def __init__(self):
        self.con = sql.connect("db/quotes.sqlite")
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS QUOTES (ID INTEGER PRIMARY KEY, NAME TEXT, QUOTE TEXT, DATE TEXT)")
        self.con.commit()

    def get_quote(self, id):
        self.c.execute("SELECT * FROM QUOTES WHERE ID = {id}".format(id=id))
        return self.c.fetchone()

    def cmd_addquote(self, message, *args):
        name = args[0].pop(0)
        date = args[0].pop()
        quote = " ".join(args[0])
        try:
            datetime.strptime(date, "%Y-%m-%d")  # try to parse the date out. else not date
        except:
            quote = (quote + " " + date).strip()
            date = ""
        quote = quote.replace("'", "''")  # Single quote escape
        self.c.execute("INSERT INTO QUOTES(QUOTE, NAME, DATE) VALUES('{q}', '{n}', '{d}')".format(q=quote,n=name, d=date))
        self.c.execute("SELECT last_insert_rowid();")
        id = self.c.fetchone()[0]
        self.con.commit()
        return "{0} added Quote #{1} to remember when {2} said \"{3}\"".format(message.author.name,  # hide '' from user
                                                                               id, name, quote.replace("''", "'"))

    def cmd_quote(self, message, *args):
        if not args[0]:
            self.c.execute("SELECT * FROM QUOTES")
            quote = random.choice(self.c.fetchall())
        else:
            try:
                self.c.execute("SELECT * FROM QUOTES WHERE ID = {id}".format(id=int(args[0][0])))
                quote = self.get_quote(args[0][0])
                if not quote: raise
            except:
                return "I could not find a quote with that ID."
        date = ""
        if quote[3] != "":
            date = datetime.strptime(quote[3], "%Y-%m-%d").strftime("%B %d, %Y")
            date = " on " + date
        return "Quote #{0}: \"{1}\" by {2}".format(quote[0], quote[2], quote[1]) + date

    def cmd_undoquote(self, *_):
        pass

    def cmd_updatequote(self, *_):
        pass

    def cmd_removequote(self, *_):
        pass

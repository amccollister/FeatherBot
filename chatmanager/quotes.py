import sqlite3 as sql
import random
from datetime import datetime
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    # TODO: removequote undoquote updatequote quote(parameter for specific number)
    def __init__(self):
        self.con = sql.connect("db/quotes.sqlite")
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS QUOTES (ID INTEGER PRIMARY KEY, NAME TEXT, QUOTE TEXT, DATE TEXT)")
        self.con.commit()

    def cmd_quoteping(self, *_):
        # return datetime.strptime("2017-05-20", "%Y-%m-%d").strftime("%B %d, %Y")
        return "\"\" ping"

    def cmd_addquote(self, message, *args):
        name = args[0].pop(0)
        date = args[0].pop()
        quote = " ".join(args[0])
        if "-" not in date:  # check to see if the final arg is actually the date
            quote = (quote + " " + date).strip()
            date = ""
        self.c.execute("INSERT INTO QUOTES(QUOTE, NAME, DATE) VALUES('{q}', '{n}', '{d}')".format(q=quote, n=name, d=date))
        self.c.execute("SELECT last_insert_rowid();")
        id = self.c.fetchone()[0]
        self.con.commit()
        return "Quote #{0} has been added for {1}: \"{2}\"".format(id, name, quote)

    def cmd_quote(self, *_):
        self.c.execute("SELECT * FROM QUOTES")
        quote = random.choice(self.c.fetchall())
        date = ""
        if quote[3] != "":
            date = datetime.strptime(quote[3], "%Y-%m-%d").strftime("%B %d, %Y")
            date = " on " + date
        return "Quote #{0}: \"{1}\" by {2}".format(quote[0], quote[2], quote[1]) + date

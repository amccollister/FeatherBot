import sqlite3 as sql
import asyncio
import parsedatetime

from datetime import timedelta
from datetime import datetime
from chatmanager import bot

# TODO reminders & remindme inputs


class Plugin(bot.ChatManager):
    reminders = []

    def __init__(self, bot):
        self.con = sql.connect("db/reminders.sqlite")
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS REMINDERS (ID INTEGER PRIMARY KEY, USER_ID TEXT, REMIND TEXT, DATE TEXT)")
        self.con.commit()
        self.bot = bot
        asyncio.async(self.check_reminders())

    @asyncio.coroutine
    async def check_reminders(self):
        while True:
            if self.reminders and self.reminders[0][1] < datetime.now(): # await bot.send_message
                await self.bot.send_message(self.reminders[0][2].channel, self.reminders[0][0])
                self.reminders.pop()
            await asyncio.sleep(1)

    async def cmd_remindme(self, message, *args):
        """
        Usage:
                !remindme [time] [message]

        Gives you a reminder some time in the future.
        """
        # Basically a copy of https://github.com/SIlver--/remindmebot-reddit

        cal = parsedatetime.Calendar()
        print(cal.parse("Oct 18 2017 to take out the trash yesterday"))
        #self.reminders.append(["This was a 5 second reminder", datetime.today() + timedelta(seconds=5), message])
        #await self.bot.send_msg(message.channel, "It worked! You'll get a reminder in 5 seconds")

    async def cmd_checkreminders(self, message, *args):
        """
        Usage:
                !checkreminders

        Displays a list of all your reminders.
        """
        self.c.execute("SELECT * FROM REMINDERS WHERE ID = {id}".format(id=message.author.id))
        self.con.commit()
        reminders = self.c.fetchall()

    async def cmd_undoreminder(self, message, *args):
        """
        Usage:
                !undoreminder

        Removes the latest reminder you added.
        """
        self.c.execute("SELECT * FROM REMINDERS WHERE ID = {id} ORDER BY ID DESC".format(id=message.author.id))
        self.con.commit()
        reminder = self.c.fetchone()
        pass

    async def cmd_removereminder(self, message, *args):
        """
        Usage:
                !removereminder <id>

        Removes one of your reminders.
        """
        r_id = None
        self.c.execute("DELETE FROM REMINDERS WHERE ID = {id}").format(id=r_id)
        self.con.commit()
        pass

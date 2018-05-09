import sqlite3 as sql
import asyncio
import parsedatetime

from datetime import timedelta
from datetime import datetime
from discord.ext import commands

# TODO reminders & remindme inputs


class ReminderCog:
    # remindme checkreminders undoreminder removereminder

    @commands.command()
    async def remindme(self, ctx):
        pass

    @commands.command()
    async def reminders(self, ctx):
        pass

    @commands.command()
    async def undoreminder(self, ctx):
        pass

    @commands.command()
    async def removereminder(self, ctx):
        pass


def setup(bot):
    bot.add_cog(ReminderCog())

'''
class Plugin(bot.ChatManager):
    def __init__(self, bot):
        self.con = sql.connect("db/reminders.sqlite")
        self.c = self.con.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS REMINDERS (ID INTEGER PRIMARY KEY, USER_ID TEXT, REMIND TEXT, DATE TEXT, CHANNEL TEXT)")
        self.con.commit()
        self.bot = bot
        asyncio.async(self.check_reminders())

    @asyncio.coroutine
    async def check_reminders(self):
        while True:
            self.c.execute("SELECT * FROM REMINDERS ORDER BY DATE ASC LIMIT 1")
            reminder = self.c.fetchone()
            if reminder and datetime.strptime(reminder[3], "%Y-%m-%d %H:%M:%S") < datetime.now():
                await self.bot.send_msg(self.bot.get_channel(reminder[4]), "<@{0}> Reminder: \"{1}\"".format(reminder[1], reminder[2]))
                self.c.execute("DELETE FROM REMINDERS WHERE ID = {id}".format(id=reminder[0]))
                self.con.commit()
            await asyncio.sleep(1)

    async def cmd_remindme(self, message, *args):
        """
        Usage:
                !remindme [time] - [message]

        Gives you a reminder some time in the future.
        Separate the time and the message with a "-"
        """
        # Basically a copy of https://github.com/SIlver--/remindmebot-reddit
        if not args[0]: return await self.bot.send_msg(message.channel, "I have nothing to remind you about.")
        arg = " ".join(args[0]).split("-")
        cal = parsedatetime.Calendar()
        time = (cal.parseDT(arg[0]))[0]
        msg = "Reminder."
        if len(arg) == 2: msg = arg[1].strip()
        self.c.execute("INSERT INTO REMINDERS ('USER_ID', 'REMIND', 'DATE', 'CHANNEL') VALUES(?, ?, ?, ?)",
                       [message.author.id, msg, time, message.channel.id])
        self.con.commit()
        await self.bot.send_msg(message.channel, "All set!\nWe'll remind you about \"{}\" on {}".format(msg, time))

    async def cmd_checkreminders(self, message, *args):
        """
        Usage:
                !checkreminders

        Displays a list of all your reminders.
        """
        self.c.execute("SELECT * FROM REMINDERS WHERE USER_ID = {id}".format(id=message.author.id))
        self.con.commit()
        reminders = self.c.fetchall()
        if not reminders:
            return await self.bot.send_msg(message.channel, "You don't have any reminders.")
        list = ""
        for r in reminders:
            list += "{:4d}  {:14s}  {}\n".format(r[0], r[2][:14], r[3])
        await self.bot.send_msg(message.channel, "```ID\tREMINDER\t\tTIME\n"
                                                 "-----------------------------------------\n{}```".format(list))

    async def cmd_undoreminder(self, message, *args):
        """
        Usage:
                !undoreminder

        Removes the latest reminder you added.
        """
        self.c.execute("SELECT * FROM REMINDERS WHERE USER_ID = {id} ORDER BY ID DESC".format(id=message.author.id))
        reminder = self.c.fetchone()
        if reminder:
            self.c.execute("DELETE FROM REMINDERS WHERE ID = {id}".format(id=reminder[0]))
            self.con.commit()
            return await self.bot.send_msg(message.channel, "Removed your \"{}\" reminder that was set for {}.".format(reminder[2], reminder[3]))
        await self.bot.send_msg(message.channel, "You don't have any reminders.")

    async def cmd_removereminder(self, message, *args):
        """
        Usage:
                !removereminder <id>

        Removes one of your reminders.
        """
        try:
            id = int(args[0][0])
        except:
            return await self.bot.send_msg(message.channel, "That's not a valid ID!")
        self.c.execute("SELECT * FROM REMINDERS WHERE ID = {id}".format(id=id))
        reminder = self.c.fetchone()
        if reminder and reminder[1] == message.author.id:
            self.c.execute("DELETE FROM REMINDERS WHERE ID = {id}".format(id=id))
            await self.bot.send_msg(message.channel, "Removed your \"{}\" reminder that was set for {}."
                                    .format(reminder[2], reminder[3]))
            self.con.commit()
        else:
            return await self.bot.send_msg(message.channel, "You don't have any reminders with that ID.")
'''
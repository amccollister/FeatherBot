import sqlite3 as sql
import random
import asyncio
from datetime import timedelta
from datetime import datetime
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    reminders = [] # reminder list
    bot = None

    def __init__(self, bot):
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
        self.reminders.append(["This was a 5 second reminder", datetime.today() + timedelta(seconds=5), message])
        await self.bot.send_message(message.channel, "It worked! You'll get a reminder in 5 seconds")

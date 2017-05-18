import discord
import random
from discord.ext.commands import Bot

class ChatManager(Bot):

    async def incoming_message(self, message : discord.Message):
        if message.content.startswith(self.command_prefix):
            args = message.content.split(" ")
            arg = args.pop(0)[1:]
            await getattr(self, "cmd_" + arg)(message, args)

    async def cmd_test(self, message, *_):
        await self.send_message(message.channel, "If you see this, Andrew did something right.")

    async def cmd_choose(self, message, *choice):
        await self.say("The best is " + random.choice(choice))

    async def cmd_hello(self, message, *_):
        await self.send_message(message.channel, "Hello I am {0}!".format(self.user.name))

    async def cmd_me(self, message, *_):
        await self.send_message(message.channel, "You are {0.author.name} in {0.channel.name}".format(message))

    async def cmd_joined(self, message, *_):
        await self.send_message(message.channel, "{0.name} joined on {0.joined_at}".format(message.author))

    async def cmd_args(self, message, *args):
        await self.send_message(message.channel, args)

    async def cmd_calc(self, message, *nums : float): # fix this # calculate command "1+1" "8%2"
        pass
        """sumNum = 0
        for i in nums:
            sumNum += i
        await self.say("The sum of all these numbers is {0}".format(sumNum))"""
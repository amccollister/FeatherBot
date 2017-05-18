import discord
from discord.ext.commands import Bot

class ChatManager(Bot):

    async def incoming_message(self, message : discord.Message):
        if message.content.startswith(self.command_prefix):
            await getattr(self, "cmd_" + message.content[1:])(message)

    async def cmd_test(self, message):
        await self.send_message(message.channel, "If you see this, Andrew did something right.")

    async def cmd_choose(self, message): # fix this
        pass  # await self.say("The best is " + random.choice(choice))

    async def cmd_hello(self, message):
        await self.send_message(message.channel, "Hello I am {0}!".format(self.user.name))

    async def cmd_me(self, message):
        await self.send_message(message.channel, "You are {0.author.name} in {0.channel.name}".format(message))

    async def cmd_joined(self, message):
        await self.send_message(message.channel, "{0.name} joined on {0.joined_at}".format(message.author))

    async def cmd_add(self, *nums: float): # fix this
        pass
        """sumNum = 0
        for i in nums:
            sumNum += i
        await self.say("The sum of all these numbers is {0}".format(sumNum))"""
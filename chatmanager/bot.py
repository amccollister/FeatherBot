import discord
import random
from discord.ext.commands import Bot

class ChatManager(Bot):
    command_list = []
    # TODO ping addquote quote currency? 8Ball Reminder Cleverbot Online motd?/rules? rngImage 1d20 RPS! facts emoteText
    # TODO wiki strawpoll youtube weather joke???
    @staticmethod
    def get_command_list():
        cmd_list = [func for func in dir(ChatManager) if str(func).startswith("cmd_")]
        return cmd_list

    def __init__(self, command_prefix, whitelist):
        super().__init__(command_prefix)
        self.whitelist = whitelist
        self.command_list = self.get_command_list()

    async def incoming_message(self, message : discord.Message):
        if message.content.startswith(self.command_prefix) and message.channel.id == self.whitelist:
                args = message.content.split(" ")
                arg = args.pop(0)[1:]
                if "cmd_" + arg in self.command_list:
                    await getattr(self, "cmd_" + arg)(message, args)
                else:
                    await self.send_message(message.channel, "```That's not a command!"
                                                             "\nPlease use !help for a list of commands.```")

    async def cmd_help(self, message, *_): #Eventually have help specific to modules
        cmds = "**Here's the current list of commands:**```"
        for cmd in self.command_list:
            cmds += (self.command_prefix + cmd[4:] + ", ")
        cmds = cmds.rstrip(", ")
        cmds += "```"
        await self.send_message(message.channel, cmds)

    async def cmd_coolest(self, message, *_):
        await self.send_message(message.channel, "{0} is the coolest!".format(message.author.name))

    async def cmd_test(self, message, *_):
        await self.send_message(message.channel, "If you see this, Andrew did something right.")

    async def cmd_choose(self, message, *choice):
        await self.send_message(message.channel, "The best is " + random.choice(choice[0]))

    async def cmd_hello(self, message, *_):
        await self.send_message(message.channel, "Hello I am {0}!".format(self.user.name))

    async def cmd_me(self, message, *_):
        await self.send_message(message.channel, "You are {0.author.name} in {0.channel.name}".format(message))

    async def cmd_joined(self, message, *_):
        await self.send_message(message.channel, "{0.name} joined on {0.joined_at}".format(message.author))
